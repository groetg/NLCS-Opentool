#include "nlcs_block_index.h"

#include <cassert>
#include <iostream>

int main(int argc, char** argv) {
    assert(argc == 3);
    nlcs::BlockIndex index;
    std::string error;
    assert(index.load(argv[1], argv[2], &error));
    assert(index.size() > 0);

    const auto choices = index.choices_for("V-SOV-LICHTMAST_STAAL-SO");
    assert(!choices.empty());
    assert(choices.front().dwg_path.filename() == "V-SOV-LICHTMAST_STAAL-SO.dwg");
    assert(!index.choices_for_library("SOV").empty());
    std::cout << "Indexed " << index.size() << " NLCS symbol records\n";
}
