#include "nlcs_panel.h"

#include "nlcs_block_index.h"

#include <QApplication>
#include <QLabel>
#include <QLineEdit>
#include <QListWidget>
#include <QFrame>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

#include <cstdlib>
#include <filesystem>
#include <memory>

namespace {

QWidget* panel = nullptr;
std::unique_ptr<QApplication> qt_application;
std::unique_ptr<nlcs::BlockIndex> block_index;
QListWidget* results = nullptr;
QLabel* details = nullptr;

std::filesystem::path data_root() {
    if (const char* value = std::getenv("NLCS_OPENTOOL_ROOT"); value && *value)
        return std::filesystem::path(value);
#ifdef NLCS_DEFAULT_ROOT
    return std::filesystem::path(NLCS_DEFAULT_ROOT);
#else
    return {};
#endif
}

void refresh_results(const QString& text) {
    results->clear();
    if (!block_index) return;
    const auto choices = block_index->search(text.toStdString());
    for (const auto& choice : choices) {
        auto* item = new QListWidgetItem(QString::fromStdString(choice.symbol));
        item->setData(Qt::UserRole, QString::fromStdString(choice.dwg_path.string()));
        if (choice.dwg_path.empty()) item->setForeground(Qt::gray);
        results->addItem(item);
    }
    if (results->count() > 0) results->setCurrentRow(0);
}

void update_details(QListWidgetItem* item) {
    if (!item) {
        details->setText("Geen symbool geselecteerd");
        return;
    }
    const auto path = item->data(Qt::UserRole).toString();
    details->setText(path.isEmpty()
        ? "DWG ontbreekt in de geindexeerde bibliotheek"
        : "DWG: " + path);
}

}  // namespace

namespace nlcs {

void show_panel() {
    if (panel) {
        panel->show();
        panel->raise();
        panel->activateWindow();
        return;
    }

    // BricsCAD normally owns the Qt application. Keep a fallback for hosts
    // that expose the BRX event loop without constructing QApplication.
    if (!QApplication::instance()) {
        static char application_name[] = "nlcs_brx";
        static char* application_argv[] = {application_name, nullptr};
        static int application_argc = 1;
        qt_application = std::make_unique<QApplication>(application_argc, application_argv);
    }

    const auto root = data_root();
    block_index = std::make_unique<BlockIndex>();
    std::string error;
    if (!block_index->load(root / "data/nlcs/tabellen/publicatie/5.02-symbolen.csv",
                     root / "data/nlcs/symbolen/autocad", &error)) {
        block_index.reset();
        return;
    }

    panel = new QWidget();
    panel->setAttribute(Qt::WA_DeleteOnClose);
    panel->setWindowTitle("NLCS Bibliotheek");
    panel->resize(520, 620);

    auto* layout = new QVBoxLayout(panel);
    auto* search = new QLineEdit(panel);
    search->setPlaceholderText("Zoek bijvoorbeeld: lichtmast");
    results = new QListWidget(panel);
    details = new QLabel("Selecteer een symbool", panel);
    details->setWordWrap(true);
    auto* preview = new QLabel("Preview\n\nWordt gekoppeld aan de DWG-preview", panel);
    preview->setAlignment(Qt::AlignCenter);
    preview->setMinimumHeight(150);
    preview->setFrameStyle(QFrame::Box | QFrame::Sunken);
    auto* insert = new QPushButton("Insert", panel);

    layout->addWidget(search);
    layout->addWidget(results);
    layout->addWidget(details);
    layout->addWidget(preview);
    layout->addWidget(insert);

    QObject::connect(search, &QLineEdit::textChanged, refresh_results);
    QObject::connect(results, &QListWidget::itemClicked, update_details);
    QObject::connect(insert, &QPushButton::clicked, [=]() {
        update_details(results->currentItem());
    });
    QObject::connect(panel, &QObject::destroyed, []() {
        panel = nullptr;
        results = nullptr;
        details = nullptr;
        block_index.reset();
    });

    search->setText("lichtmast");
    panel->show();
}

}  // namespace nlcs
