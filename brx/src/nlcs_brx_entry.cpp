#ifndef _WIN32
#include "brx_platform_linux.h"
#endif

#include "arxHeaders.h"

#include "nlcs_block_index.h"
#ifdef NLCS_ENABLE_QT_PANEL
#include "nlcs_panel.h"
#endif

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <filesystem>
#include <string>

namespace {

std::string layer_name_for_symbol(std::string symbol) {
    // Symbol names use a status/view prefix and an S-library prefix. Object
    // layers use the discipline code, a user status prefix, and -S for a
    // symbol object: V-SOV-LICHTMAST...-SO -> N-OV-LICHTMAST-S.
    if (symbol.size() > 2 && symbol[1] == '-') symbol.erase(0, 2);
    // Symbol libraries are named S<NLCS-discipline>, e.g. SOV or SRI.
    if (symbol.size() > 4 && symbol[0] == 'S' && symbol[3] == '-')
        symbol.erase(0, 1);
    if (symbol.size() > 3 && symbol.compare(symbol.size() - 3, 3, "-SO") == 0)
        symbol.erase(symbol.size() - 3);
    const auto separator = symbol.find('-');
    if (separator != std::string::npos) symbol.erase(0, separator + 1);
    return symbol;
}

std::wstring wide_string(const std::string& value) {
    return std::wstring(value.begin(), value.end());
}

}  // namespace

class NlcsBrxApp final : public AcRxArxApp {
public:
    NlcsBrxApp() : AcRxArxApp() {}

    void RegisterServerComponents() override {}
    static void NLCSAppNLCS();
    static void NLCSAppNLCSBlocks();
    static void NLCSAppNLCSInsert();

    AcRx::AppRetCode On_kInitAppMsg(void* app_data) override {
        const auto result = AcRxArxApp::On_kInitAppMsg(app_data);
        acrxRegisterAppMDIAware(app_data);
        acrxUnlockApplication(app_data);
        acutPrintf(_T("\n[NLCS] BRX-module geladen. Gebruik NLCS om te starten.\n"));
        return result;
    }
};

IMPLEMENT_ARX_ENTRYPOINT(NlcsBrxApp)

ACED_ARXCOMMAND_ENTRY_AUTO(NlcsBrxApp, NLCSApp, NLCS, NLCS, ACRX_CMD_MODAL, nullptr)
ACED_ARXCOMMAND_ENTRY_AUTO(NlcsBrxApp, NLCSApp, NLCSBlocks, NLCSBlocks, ACRX_CMD_MODAL, nullptr)
ACED_ARXCOMMAND_ENTRY_AUTO(NlcsBrxApp, NLCSApp, NLCSInsert, NLCSInsert, ACRX_CMD_MODAL, nullptr)

void NlcsBrxApp::NLCSAppNLCS() {
#ifdef NLCS_ENABLE_QT_PANEL
    nlcs::show_panel();
#else
    acutPrintf(_T("\n[NLCS] BRX-core actief. De Qt-panel is uitgeschakeld op Linux.\n"));
#endif
}

void NlcsBrxApp::NLCSAppNLCSBlocks() {
    const char* root_value = std::getenv("NLCS_OPENTOOL_ROOT");
#ifdef NLCS_DEFAULT_ROOT
    const std::filesystem::path root = root_value && *root_value != '\0'
        ? std::filesystem::path(root_value)
        : std::filesystem::path(NLCS_DEFAULT_ROOT);
#else
    if (!root_value || *root_value == '\0') {
        acutPrintf(_T("\n[NLCS] Zet NLCS_OPENTOOL_ROOT op de projectmap en probeer opnieuw.\n"));
        return;
    }
    const std::filesystem::path root(root_value);
#endif
    nlcs::BlockIndex index;
    std::string error;
    if (!index.load(root / "data/nlcs/tabellen/publicatie/5.02-symbolen.csv",
                    root / "data/nlcs/symbolen/autocad", &error)) {
        acutPrintf(_T("\n[NLCS] %s\n"), error.c_str());
        return;
    }

    std::size_t resolved = 0;
    for (const auto& choice : index.choices_for_library("SOV"))
        if (!choice.dwg_path.empty()) ++resolved;
    acutPrintf(_T("\n[NLCS] %lu symbolrecords geindexeerd; SOV: %lu gekoppeld.\n"),
               static_cast<unsigned long>(index.size()),
               static_cast<unsigned long>(resolved));
}

void NlcsBrxApp::NLCSAppNLCSInsert() {
    const char* root_value = std::getenv("NLCS_OPENTOOL_ROOT");
#ifdef NLCS_DEFAULT_ROOT
    const std::filesystem::path root = root_value && *root_value != '\0'
        ? std::filesystem::path(root_value)
        : std::filesystem::path(NLCS_DEFAULT_ROOT);
#else
    if (!root_value || *root_value == '\0') {
        acutPrintf(_T("\n[NLCS] Zet NLCS_OPENTOOL_ROOT op de projectmap en probeer opnieuw.\n"));
        return;
    }
    const std::filesystem::path root(root_value);
#endif

    ACHAR status_buffer[64] = {};
    if (acedGetString(false,
                      _T("\nStatus (N=Nieuw, B=Bestaand, V=Vervallen, T=Tijdelijk, R=Revisie): "),
                      status_buffer) != RTNORM)
        return;
    std::string status;
    for (const ACHAR* cursor = status_buffer; *cursor != 0; ++cursor)
        status.push_back(static_cast<char>(
            std::toupper(static_cast<unsigned char>(*cursor))));
    if (status != "N" && status != "B" && status != "V" &&
        status != "T" && status != "R") {
        acutPrintf(_T("\n[NLCS] Ongeldige statusprefix. Gebruik N, B, V, T of R.\n"));
        return;
    }

    ACHAR discipline_buffer[64] = {};
    if (acedGetString(false,
                      _T("\nDiscipline (WE=Wegen, RI=Riolering, OV=Openbare verlichting): "),
                      discipline_buffer) != RTNORM)
        return;
    std::string discipline;
    for (const ACHAR* cursor = discipline_buffer; *cursor != 0; ++cursor)
        discipline.push_back(static_cast<char>(
            std::toupper(static_cast<unsigned char>(*cursor))));
    if (discipline.empty()) {
        acutPrintf(_T("\n[NLCS] Discipline is verplicht.\n"));
        return;
    }

    ACHAR symbol_buffer[512] = {};
    if (acedGetString(false, _T("\nZoek in NLCS-bibliotheek: "), symbol_buffer) != RTNORM)
        return;

    std::string symbol;
    for (const ACHAR* cursor = symbol_buffer; *cursor != 0; ++cursor)
        symbol.push_back(static_cast<char>(*cursor));

    nlcs::BlockIndex index;
    std::string error;
    if (!index.load(root / "data/nlcs/tabellen/publicatie/5.02-symbolen.csv",
                    root / "data/nlcs/symbolen/autocad", &error)) {
        acutPrintf(_T("\n[NLCS] %s\n"), error.c_str());
        return;
    }

    const auto choices = index.search(symbol);
    if (choices.empty()) {
        acutPrintf(_T("\n[NLCS] Geen bibliotheekresultaten voor %s.\n"), symbol.c_str());
        return;
    }

    const int shown = static_cast<int>(std::min<std::size_t>(choices.size(), 20));
    acutPrintf(_T("\n[NLCS] Resultaten voor %s:\n"), symbol.c_str());
    for (int i = 0; i < shown; ++i) {
        acutPrintf(_T("  %d. %s%s\n"), i + 1, choices[i].symbol.c_str(),
                   choices[i].dwg_path.empty() ? _T(" [DWG ontbreekt]") : _T(""));
    }

    int selected = 0;
    if (acedGetIntInRange(_T("\nKies symboolnummer: "), &selected, 1, shown) != RTNORM)
        return;
    const auto& choice = choices[static_cast<std::size_t>(selected - 1)];
    if (choice.dwg_path.empty()) {
        acutPrintf(_T("\n[NLCS] Voor dit symbool is geen DWG-bestand gevonden.\n"));
        return;
    }

    const std::string layer_name = status + "-" + discipline + "-" +
                                   layer_name_for_symbol(choice.symbol) + "-S";
    const std::wstring wide_layer = wide_string(layer_name);
    acutPrintf(_T("\n[NLCS] Layer: %s\n"), layer_name.c_str());
    acedCommandS(RTSTR, _T("_.-LAYER"), RTSTR, _T("_M"),
                 RTSTR, wide_layer.c_str(), RTNONE);

    ads_point point;
    if (acedGetPoint(nullptr, _T("\nInvoegpunt: "), point) != RTNORM)
        return;

    const std::string path = choice.dwg_path.string();
    const std::wstring wide_path = wide_string(path);
    acedCommandS(RTSTR, _T("_.-INSERT"), RTSTR, wide_path.c_str(),
                 RT3DPOINT, point, RTREAL, 1.0, RTREAL, 0.0, RTNONE);
}
