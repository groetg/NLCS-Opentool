#include "nlcs_block_index.h"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <sstream>
#include <unordered_map>

namespace {

std::vector<std::string> parse_nlcs_row(const std::string& line) {
    // NLCS 5.02 exports one quoted record whose fields are separated by
    // comma-double-quote (rather than ordinary RFC 4180 quoting).
    std::vector<std::string> fields;
    std::string field;
    for (std::size_t i = 0; i < line.size();) {
        if (i + 2 < line.size() && line[i] == ',' && line[i + 1] == '"' &&
            line[i + 2] == '"') {
            fields.push_back(field);
            field.clear();
            i += 3;
            continue;
        }
        field += line[i++];
    }
    fields.push_back(field);

    for (auto& value : fields) {
        // The export wraps the complete record in quotes, while individual
        // fields use doubled quotes. Strip the record wrapper independently.
        while (!value.empty() && value.front() == '"') value.erase(value.begin());
        while (!value.empty() && value.back() == '"') value.pop_back();
        value.erase(std::remove(value.begin(), value.end(), '\r'), value.end());
        std::string unescaped;
        for (std::size_t i = 0; i < value.size(); ++i) {
            if (i + 1 < value.size() && value[i] == '"' && value[i + 1] == '"') {
                unescaped += '"';
                ++i;
            } else {
                unescaped += value[i];
            }
        }
        value = std::move(unescaped);
    }
    return fields;
}

std::string key_for(const std::string& value) {
    std::string key = value;
    std::transform(key.begin(), key.end(), key.begin(),
                   [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
    return key;
}

bool contains_insensitive(const std::string& value, const std::string& text) {
    return key_for(value).find(key_for(text)) != std::string::npos;
}

}  // namespace

namespace nlcs {

bool BlockIndex::load(const std::filesystem::path& symbol_csv,
                      const std::filesystem::path& dwg_root,
                      std::string* error) {
    choices_.clear();
    std::ifstream input(symbol_csv);
    if (!input) {
        if (error) *error = "Kan symbolentabel niet openen: " + symbol_csv.string();
        return false;
    }

    std::unordered_map<std::string, std::filesystem::path> dwgs;
    if (std::filesystem::exists(dwg_root)) {
        for (const auto& entry : std::filesystem::recursive_directory_iterator(dwg_root)) {
            if (!entry.is_regular_file() || entry.path().extension() != ".dwg") continue;
            dwgs.emplace(key_for(entry.path().stem().string()), entry.path());
        }
    }

    std::string line;
    std::getline(input, line);  // header
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        const auto fields = parse_nlcs_row(line);
        if (fields.size() < 8 || fields[5].empty()) continue;

        SymbolChoice choice{fields[5], fields[2], fields[6], {}};
        const auto found = dwgs.find(key_for(choice.symbol));
        if (found != dwgs.end()) choice.dwg_path = found->second;
        choices_.push_back(std::move(choice));
    }

    std::sort(choices_.begin(), choices_.end(), [](const auto& left, const auto& right) {
        if (left.symbol != right.symbol) return left.symbol < right.symbol;
        return left.option < right.option;
    });
    return true;
}

std::vector<SymbolChoice> BlockIndex::choices_for(const std::string& symbol) const {
    std::vector<SymbolChoice> result;
    for (const auto& choice : choices_)
        if (key_for(choice.symbol) == key_for(symbol)) result.push_back(choice);
    return result;
}

std::vector<SymbolChoice> BlockIndex::choices_for_library(const std::string& library) const {
    std::vector<SymbolChoice> result;
    for (const auto& choice : choices_)
        if (key_for(choice.library) == key_for(library)) result.push_back(choice);
    return result;
}

std::vector<SymbolChoice> BlockIndex::search(const std::string& text) const {
    std::vector<SymbolChoice> result;
    for (const auto& choice : choices_) {
        if (contains_insensitive(choice.symbol, text)) result.push_back(choice);
    }
    return result;
}

}  // namespace nlcs
