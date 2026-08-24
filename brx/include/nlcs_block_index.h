#pragma once

#include <filesystem>
#include <string>
#include <vector>

namespace nlcs {

struct SymbolChoice {
    std::string symbol;
    std::string library;
    std::string option;
    std::filesystem::path dwg_path;
};

class BlockIndex {
public:
    // Read 5.02-symbolen.csv and match its symbol names to DWG file stems.
    // Missing DWGs are retained as unresolved choices so the UI can report
    // incomplete installations instead of silently inventing a path.
    bool load(const std::filesystem::path& symbol_csv,
              const std::filesystem::path& dwg_root,
              std::string* error = nullptr);

    std::vector<SymbolChoice> choices_for(const std::string& symbol) const;
    std::vector<SymbolChoice> choices_for_library(const std::string& library) const;
    std::vector<SymbolChoice> search(const std::string& text) const;
    std::size_t size() const { return choices_.size(); }

private:
    std::vector<SymbolChoice> choices_;
};

}  // namespace nlcs
