import json
import os

def build_merged_app():
    json_path = r"c:\Users\Acer\Desktop\deneme analiz p\current_database.json"
    html_out_path = r"c:\Users\Acer\Desktop\ceylanpinar-portal\index.html"
    
    print(f"Reading JSON database from: {json_path}")
    if not os.path.exists(json_path):
        print("JSON database not found! Run process_data.py first.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        database_records = json.load(f)
        
    records_js_str = json.dumps(database_records, ensure_ascii=False)
    
    html_template = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ceylanpınar Fen Lisesi - Portal Hub</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- SheetJS for Excel Reading -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    
    <!-- Chart.js for beautiful graphs -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --accent-gradient: linear-gradient(135deg, #4f46e5, #7c3aed);
            --accent-color: #4f46e5;
            --accent-hover: #4338ca;
            --net-bg: #dcfce7;
            --net-text: #15803d;
            --success-color: #10b981;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            --radius-md: 12px;
            --radius-lg: 20px;
        }

        [data-theme="dark"] {
            --bg-page: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --accent-gradient: linear-gradient(135deg, #6366f1, #a855f7);
            --accent-color: #6366f1;
            --accent-hover: #4f46e5;
            --net-bg: #064e3b;
            --net-text: #4ade80;
            --success-color: #34d399;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Header Style */
        header {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
        }

        .logo-icon {
            background: transparent;
            padding: 0;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            overflow: hidden;
        }

        .logo-img {
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
        }

        .logo-title {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin-bottom: 0.15rem;
        }

        .logo-subtitle {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
            line-height: 1.2;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.625rem 1.25rem;
            border-radius: var(--radius-md);
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
        }

        .btn-primary {
            background: var(--accent-gradient);
            color: white;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
        }

        .btn-primary:hover {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
        }

        .btn-secondary {
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .btn-secondary:hover {
            background: var(--border-color);
        }

        .theme-toggle {
            background: none;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.5rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .theme-toggle:hover {
            background: var(--border-color);
        }

        /* Layout Grid */
        .app-container {
            display: grid;
            grid-template-columns: 320px 1fr;
            flex-grow: 1;
            min-height: calc(100vh - 80px);
        }

        .app-container.no-sidebar {
            grid-template-columns: 1fr;
        }

        .app-container.no-sidebar aside {
            display: none;
        }

        /* Sidebar (Desktop Only) */
        aside {
            background: var(--bg-card);
            border-right: 1px solid var(--border-color);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            overflow-y: auto;
        }

        .sidebar-card {
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
        }

        .sidebar-card h3 {
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }

        .stat-card-small {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.75rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .stat-card-small .val {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .stat-card-small .lbl {
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* Dropzone */
        .dropzone {
            border: 2px dashed var(--border-color);
            border-radius: var(--radius-md);
            padding: 1.5rem 1rem;
            text-align: center;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            background: var(--bg-card);
            transition: all 0.2s ease;
        }

        .dropzone:hover, .dropzone.dragover {
            border-color: var(--accent-color);
            background: rgba(79, 70, 229, 0.03);
        }

        .dropzone-icon {
            color: var(--accent-color);
        }

        .dropzone p {
            font-size: 0.75rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .dropzone input {
            display: none;
        }

        /* Main Content */
        main {
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            overflow-y: auto;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
            justify-content: center;
        }

        .app-container:not(.no-sidebar) main {
            justify-content: flex-start;
        }

        /* Selection Screen */
        .portal-selection {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 3rem;
            align-items: start;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            animation: fadeIn 0.4s ease;
        }

        .portal-welcome {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }

        .welcome-logo {
            width: 90px;
            height: 90px;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.06));
        }

        .portal-welcome h2 {
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .portal-welcome p {
            font-size: 1.05rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .selection-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            width: 100%;
        }

        .selection-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 3rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 1.5rem;
            cursor: pointer;
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .selection-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent-color);
        }

        .selection-card-icon {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: rgba(79, 70, 229, 0.08);
            color: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .selection-card:hover .selection-card-icon {
            background: var(--accent-gradient);
            color: white;
        }

        .selection-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .selection-card p {
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* Hub Section (Hidden by Default) */
        .hub-section {
            display: none;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            animation: fadeIn 0.4s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .hub-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            margin-bottom: 3rem;
        }

        .hub-title-area h2 {
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }

        .hub-title-area p {
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .portal-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            width: 100%;
        }

        /* Portal Card */
        .portal-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 2.25rem 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            text-decoration: none;
            color: inherit;
            cursor: pointer;
        }

        .portal-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--accent-gradient);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .portal-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent-color);
        }

        .portal-card:hover::before {
            opacity: 1;
        }

        .card-icon-wrapper {
            width: 50px;
            height: 50px;
            border-radius: var(--radius-md);
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            color: var(--accent-color);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .portal-card:hover .card-icon-wrapper {
            background: var(--accent-gradient);
            color: white;
            border-color: transparent;
        }

        .card-content h3 {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .card-content p {
            font-size: 0.875rem;
            color: var(--text-secondary);
            line-height: 1.5;
            font-weight: 500;
        }

        .badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 50px;
            background: rgba(79, 70, 229, 0.08);
            color: var(--accent-color);
            border: 1px solid rgba(79, 70, 229, 0.15);
        }

        .badge-disabled {
            background: var(--bg-page);
            color: var(--text-secondary);
            border-color: var(--border-color);
        }

        .card-action {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--accent-color);
            margin-top: auto;
        }

        .portal-card-disabled {
            opacity: 0.75;
            cursor: not-allowed;
        }
        
        .portal-card-disabled:hover {
            transform: none;
            box-shadow: var(--shadow-md);
            border-color: var(--border-color);
        }

        .portal-card-disabled:hover::before {
            opacity: 0;
        }

        /* Password Modal */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.4);
            backdrop-filter: blur(4px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s ease;
        }

        .modal.open {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 2.5rem;
            width: 100%;
            max-width: 440px;
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            transform: scale(0.95);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .modal.open .modal-card {
            transform: scale(1);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h3 {
            font-size: 1.25rem;
            font-weight: 700;
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .input-group label {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .input-field {
            width: 100%;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-color);
            background: var(--bg-page);
            color: var(--text-primary);
            outline: none;
            font-size: 1rem;
            font-weight: 500;
        }

        .input-field:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        .error-message {
            color: #ef4444;
            font-size: 0.8125rem;
            font-weight: 600;
            display: none;
        }

        /* ---------------------------------------------------- */
        /* EXAM ANALYSIS SPECIFIC STYLES */
        /* ---------------------------------------------------- */
        
        .analysis-section {
            display: none;
            flex-direction: column;
            gap: 2rem;
            width: 100%;
            animation: fadeIn 0.4s ease;
        }

        /* Search Section */
        .search-container {
            position: relative;
            z-index: 50;
        }

        .search-box-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            color: var(--text-secondary);
            pointer-events: none;
        }

        .search-input {
            width: 100%;
            padding: 1rem 1rem 1rem 3rem;
            font-size: 1rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
            outline: none;
            font-weight: 500;
        }

        .search-input:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        /* Autocomplete Dropdown */
        .search-results {
            position: absolute;
            top: calc(100% + 4px);
            left: 0;
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            max-height: 250px;
            overflow-y: auto;
            box-shadow: var(--shadow-lg);
            display: none;
        }

        .search-result-item {
            padding: 0.75rem 1.25rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 500;
            border-bottom: 1px solid var(--border-color);
        }

        .search-result-item:last-child {
            border-bottom: none;
        }

        .search-result-item:hover, .search-result-item.selected {
            background: rgba(79, 70, 229, 0.05);
            color: var(--accent-color);
        }

        .search-result-item .meta {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        /* Info Card */
        .info-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .info-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1rem;
        }

        .student-details h2 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }

        .student-meta {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .badge-accent {
            background: rgba(79, 70, 229, 0.1);
            color: var(--accent-color);
            border-color: rgba(79, 70, 229, 0.2);
        }

        /* Table Responsive */
        .table-container {
            width: 100%;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.8125rem;
        }

        th, td {
            padding: 0.625rem 0.75rem;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }

        th {
            background: var(--bg-page);
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.02em;
        }

        /* Subheader alignment */
        tr.subheader-row th {
            padding: 0.35rem 0.75rem;
            font-weight: 700;
            font-size: 0.7rem;
            text-align: center;
        }

        td.cell-net, th.cell-net-header {
            background: var(--net-bg) !important;
            color: var(--net-text) !important;
            font-weight: 700;
            text-align: center;
        }
        
        td.cell-score {
            font-weight: 700;
            color: var(--accent-color);
        }

        td.cell-rank {
            font-weight: 600;
        }

        tr.total-row td {
            background: var(--bg-page);
            font-weight: 700;
            border-top: 2px solid var(--border-color);
            border-bottom: none;
        }

        /* Charts Container */
        .charts-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .chart-card h3 {
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chart-wrapper {
            position: relative;
            width: 100%;
            height: 350px;
        }

        /* Status Toast */
        .toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #1e293b;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            opacity: 0;
            transform: translateY(1rem);
            pointer-events: none;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
            pointer-events: auto;
        }

        .toast-success {
            border-left: 4px solid var(--success-color);
        }

        /* Utilities */
        .mobile-only {
            display: none !important;
        }

        /* Mobile Bottom Nav Bar */
        .mobile-nav-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 64px;
            background: var(--bg-card);
            border-top: 1px solid var(--border-color);
            display: none;
            justify-content: space-around;
            align-items: center;
            z-index: 999;
            box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
            padding: 0 0.5rem;
        }

        .mobile-nav-item {
            background: none;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            font-size: 0.6875rem;
            font-weight: 600;
            gap: 0.25rem;
            flex-grow: 1;
            height: 100%;
            cursor: pointer;
            transition: color 0.2s ease;
        }

        .mobile-nav-item i {
            width: 20px;
            height: 20px;
            transition: transform 0.2s ease;
        }

        .mobile-nav-item:active i {
            transform: scale(0.9);
        }

        .mobile-nav-item.active {
            color: var(--accent-color);
        }

        /* Print CSS Styling */
        @media print {
            body, html {
                background: white !important;
                color: black !important;
            }

            header, aside, .search-container, .btn, .header-actions, .theme-toggle, .dropzone, .sidebar-card, .toast, .portal-selection, .hub-section, .mobile-nav-bar {
                display: none !important;
            }

            .app-container {
                display: block !important;
                min-height: auto !important;
            }

            main {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
                width: 100% !important;
                background: white !important;
            }

            .analysis-section {
                display: flex !important;
            }

            .info-card {
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                background: white !important;
                page-break-after: avoid;
            }

            .table-container {
                border: 1px solid #000000 !important;
            }

            table {
                border-collapse: collapse !important;
                width: 100% !important;
            }

            th, td {
                border: 1px solid #000000 !important;
                color: black !important;
                background: transparent !important;
                padding: 4px 6px !important;
            }

            td.cell-net, th.cell-net-header {
                background: #f1f5f9 !important;
                color: black !important;
                border: 1px solid #000000 !important;
            }

            .chart-card {
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                margin-top: 20px !important;
                page-break-inside: avoid;
            }

            .chart-wrapper {
                height: 250px !important;
            }
        }

        /* Responsive CSS Rules */
        @media (max-width: 1024px) {
            .app-container {
                display: flex;
                flex-direction: column;
            }

            main {
                order: 1; /* Main content first on mobile */
            }

            aside {
                order: 2; /* Sidebar (Stats, Settings) at the bottom on mobile */
                border-right: none;
                border-top: 1px solid var(--border-color);
                border-bottom: none;
                flex-direction: row;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .sidebar-card {
                flex: 1 1 280px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (max-width: 768px) {
            .mobile-only {
                display: block !important;
            }
            
            .mobile-flex-only {
                display: flex !important;
            }

            .desktop-only {
                display: none !important;
            }

            .mobile-nav-bar {
                display: flex;
            }

            body {
                padding-bottom: 64px; /* Room for bottom bar */
            }

            /* Hide Desktop Sidebar in Mobile view altogether */
            aside {
                display: none !important;
            }

            .app-container {
                grid-template-columns: 1fr;
            }

            header {
                padding: 0.75rem 1rem;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                gap: 0.5rem;
            }

            .logo-title {
                font-size: 0.95rem !important;
            }

            .logo-subtitle {
                font-size: 0.7rem !important;
            }

            .logo-icon {
                width: 45px !important;
                height: 45px !important;
            }

            .header-actions {
                gap: 0.5rem;
            }

            .btn span {
                display: none; /* Hide text on mobile */
            }

            .btn {
                padding: 0.5rem 0.75rem;
                border-radius: var(--radius-md);
                font-size: 0.8rem;
            }

            main {
                padding: 1rem;
                gap: 1rem;
            }

            .info-card {
                padding: 1rem;
                border-radius: var(--radius-md);
            }

            .info-card-header {
                flex-direction: column;
                gap: 1rem;
                align-items: stretch;
            }

            .info-card-header .btn {
                width: 100%;
                justify-content: center;
                height: 44px !important;
            }

            .student-meta {
                flex-wrap: wrap;
                gap: 0.5rem;
            }

            .chart-card {
                padding: 1rem;
            }

            .chart-wrapper {
                height: 250px;
            }

            /* Slim down selection cards for mobile */
            .selection-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .selection-card {
                padding: 1.75rem 1.25rem;
                gap: 0.75rem;
                border-radius: var(--radius-md);
            }

            .selection-card h3 {
                font-size: 1.2rem;
            }

            .selection-card p {
                font-size: 0.8rem;
            }

            .selection-card-icon {
                width: 55px;
                height: 55px;
            }

            .selection-card-icon i {
                width: 24px;
                height: 24px;
            }

            .portal-selection {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }

            .portal-welcome h2 {
                font-size: 1.75rem;
            }

            .portal-welcome p {
                font-size: 0.9rem;
            }

            /* Adjust search container and input sizes on mobile */
            .search-container input, #search-student {
                height: 44px !important;
                font-size: 0.85rem;
            }

            #teacher-analysis-view button {
                height: 44px !important;
                padding: 0 1rem;
            }

            /* Announcements mobile adjustments */
            .announcements-card {
                padding: 1.25rem;
                gap: 1rem;
                border-radius: var(--radius-md);
            }

            .announcements-card h3 {
                font-size: 1.1rem;
            }

            .announcement-item h4 {
                font-size: 0.875rem;
            }

            .announcement-item p {
                font-size: 0.8rem;
            }
        }

        /* Announcements Styles */
        .announcements-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 2rem;
            box-shadow: var(--shadow-md);
            text-align: left;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            width: 100%;
        }

        .announcements-card h3 {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
        }

        .announcements-list {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .announcement-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px dashed var(--border-color);
        }

        .announcement-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .announcement-date {
            font-size: 0.72rem;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .announcement-item h4 {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .announcement-item p {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-section" onclick="handleLogoClick()">
            <div class="logo-icon" id="logo-container">
                <img id="logo-img" class="logo-img" src="logo.png" alt="Logo">
            </div>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h1 class="logo-title">Ceylanpınar Fen Lisesi</h1>
                <p class="logo-subtitle" id="header-subtitle">Portal Hub</p>
            </div>
        </div>
        <div class="header-actions">
            <button class="btn btn-secondary" id="logout-btn" style="display:none;" onclick="logout()">
                <i data-lucide="log-out"></i> <span>Çıkış Yap</span>
            </button>
            <button class="theme-toggle" id="theme-btn" onclick="toggleTheme()" title="Temayı Değiştir">
                <i data-lucide="moon"></i>
            </button>
        </div>
    </header>

    <div class="app-container no-sidebar" id="app-container">
        <!-- Sidebar (Desktop Only - Hidden in Mobile View) -->
        <aside class="desktop-only">
            <!-- Sınav Yükleme -->
            <div class="sidebar-card">
                <h3><i data-lucide="file-plus"></i> Sınav İçe Aktar</h3>
                <div class="dropzone" id="excel-dropzone" onclick="document.getElementById('excel-file-input').click()">
                    <div class="dropzone-icon">
                        <i data-lucide="file-spreadsheet" size="32"></i>
                    </div>
                    <strong>Excel Dosyası Seç</strong>
                    <p>TYT Sonuç dosyasını (xlsx/xlsm) buraya sürükleyin veya tıklayın</p>
                    <input type="file" id="excel-file-input" accept=".xlsx,.xlsm" onchange="handleExcelImport(event)">
                </div>
            </div>

            <!-- İstatistik Kartları -->
            <div class="sidebar-card">
                <h3><i data-lucide="bar-chart-2"></i> Sistem İstatistikleri</h3>
                <div class="stats-grid">
                    <div class="stat-card-small">
                        <span class="val" id="stat-students">0</span>
                        <span class="lbl">Kayıtlı Öğrenci</span>
                    </div>
                    <div class="stat-card-small">
                        <span class="val" id="stat-exams">0</span>
                        <span class="lbl">Toplam Deneme</span>
                    </div>
                    <div class="stat-card-small">
                        <span class="val" id="stat-avg-net">0.00</span>
                        <span class="lbl">Okul Genel Net Ort.</span>
                    </div>
                </div>
            </div>

            <!-- Veri Yönetimi -->
            <div class="sidebar-card">
                <h3><i data-lucide="settings"></i> Sistem Ayarları</h3>
                <button class="btn btn-secondary" style="width:100%; border-color:#ef4444; color:#ef4444;" onclick="resetToDefault()" title="Tüm verileri silip varsayılan veriye döner">
                    <i data-lucide="rotate-ccw"></i> Fabrika Ayarlarına Dön
                </button>
            </div>
        </aside>

        <main>
            <!-- 1. Seçim Ekranı -->
            <div class="portal-selection" id="selection-screen">
                <!-- Sol Taraf: Giriş Alanları (Tab-1 in Mobile) -->
                <div id="portal-tab-home" style="display: flex; flex-direction: column; gap: 2rem; width: 100%;">
                    <div class="portal-welcome">
                        <img class="welcome-logo" src="logo.png" alt="Okul Logosu">
                        <h2>Ceylanpınar Fen Lisesi</h2>
                        <p>Uygulama Seçim Portalı</p>
                    </div>

                    <div class="selection-grid">
                        <!-- Öğretmen Kartı -->
                        <div class="selection-card" onclick="openLoginModal()">
                            <div class="selection-card-icon">
                                <i data-lucide="user-cog" size="36"></i>
                            </div>
                            <h3>Öğretmen Girişi</h3>
                            <p>Sınav analizi, öğrenci takibi ve diğer yönetimsel araçlara erişmek için şifreyle giriş yapın.</p>
                        </div>

                        <!-- Öğrenci Kartı -->
                        <div class="selection-card" onclick="showStudentHub()">
                            <div class="selection-card-icon">
                                <i data-lucide="graduation-cap" size="36"></i>
                            </div>
                            <h3>Öğrenci Girişi</h3>
                            <p>Sınav sonuçlarınızı incelemek, ders programlarınızı görmek ve karnelerinize erişmek için tıklayın.</p>
                        </div>
                    </div>
                </div>

                <!-- Sağ Taraf: Duyurular & Haberler (Tab-2 in Mobile, Hidden in desktop if mobile-tab-announcements is selected) -->
                <div id="portal-tab-announcements" class="announcements-card">
                    <h3><i data-lucide="megaphone" style="color:var(--accent-color);"></i> Duyurular & Haberler</h3>
                    <div class="announcements-list">
                        <div class="announcement-item">
                            <span class="announcement-date">02 Temmuz 2026</span>
                            <h4>Deneme Analiz Sistemi Güncellendi</h4>
                            <p>Deneme sınav takip sistemi yeni tasarımı ve güvenlik altyapısı ile yayına alınmıştır.</p>
                        </div>
                        <div class="announcement-item">
                            <span class="announcement-date">28 Haziran 2026</span>
                            <h4>Yaz Dönemi Destekleme Kursları</h4>
                            <p>12. sınıf öğrencilerimiz için ders programları öğretmen portalı üzerinden yakında paylaşılacaktır.</p>
                        </div>
                        <div class="announcement-item">
                            <span class="announcement-date">15 Haziran 2026</span>
                            <h4>YKS Tercih Danışmanlığı</h4>
                            <p>Okulumuz rehberlik servisi tercih dönemi boyunca velilerimize ve öğrencilerimize hizmet verecektir.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2. Öğretmen Hub (Menü) -->
            <div class="hub-section" id="teacher-hub">
                <div class="hub-header">
                    <div class="hub-title-area">
                        <h2>Öğretmen ve Yönetici Portalı</h2>
                        <p>Analiz ve yönetim uygulamaları</p>
                    </div>
                </div>
                <div class="portal-grid">
                    <!-- Sınav Analiz Kartı -->
                    <div class="portal-card" onclick="showTeacherAnalysisView()">
                        <div class="card-icon-wrapper">
                            <i data-lucide="bar-chart-3" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Deneme Analiz Sistemi <span class="badge">Aktif</span></h3>
                            <p>Deneme sınav sonuçlarını veri tabanına yükleyin, öğrenci karneleri çıkartın ve gelişim istatistiklerini takip edin.</p>
                        </div>
                        <div class="card-action">
                            Sisteme Giriş Yap <i data-lucide="arrow-right" size="16"></i>
                        </div>
                    </div>

                    <!-- Rehberlik Kartı (Placeholder) -->
                    <div class="portal-card portal-card-disabled">
                        <div class="card-icon-wrapper">
                            <i data-lucide="users" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Rehberlik & Öğrenci Takip <span class="badge badge-disabled">Yakında</span></h3>
                            <p>Öğrenci görüşmelerini, sınıf rehberlik notlarını ve davranış gelişim kayıtlarını dijital olarak tutun.</p>
                        </div>
                        <div class="card-action" style="color: var(--text-secondary);">
                            Kullanıma Kapalı <i data-lucide="lock" size="16"></i>
                        </div>
                    </div>

                    <!-- Program Kartı (Placeholder) -->
                    <div class="portal-card portal-card-disabled">
                        <div class="card-icon-wrapper">
                            <i data-lucide="calendar" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Ders Programı & Nöbetler <span class="badge badge-disabled">Yakında</span></h3>
                            <p>Haftalık ders programlarını, nöbet çizelgelerini ve öğretmen izin/yedek planlamalarını yönetin.</p>
                        </div>
                        <div class="card-action" style="color: var(--text-secondary);">
                            Kullanıma Kapalı <i data-lucide="lock" size="16"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Öğrenci Paneli -->
            <div class="hub-section" id="student-hub">
                <div class="hub-header">
                    <div class="hub-title-area">
                        <h2>Öğrenci Bilgi Portalı</h2>
                        <p>Kişisel sınav ve başarı takibi</p>
                    </div>
                </div>
                <div class="portal-grid">
                    <!-- Deneme Sonuç Sorgulama Kartı -->
                    <div class="portal-card portal-card-disabled">
                        <div class="card-icon-wrapper">
                            <i data-lucide="search" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Sınav Sonuç Sorgulama <span class="badge badge-disabled">Yakında</span></h3>
                            <p>Öğrenci numaranızla giriş yaparak deneme sınav sonuçlarınızı ve gelişim grafiklerinizi inceleyin.</p>
                        </div>
                        <div class="card-action" style="color: var(--text-secondary);">
                            Kullanıma Kapalı <i data-lucide="lock" size="16"></i>
                        </div>
                    </div>

                    <!-- Haftalık Ders Programı Kartı -->
                    <div class="portal-card portal-card-disabled">
                        <div class="card-icon-wrapper">
                            <i data-lucide="calendar-days" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Haftalık Ders Programı <span class="badge badge-disabled">Yakında</span></h3>
                            <p>Sınıfınızın haftalık güncel ders saatlerini ve öğretmen programlarını takip edin.</p>
                        </div>
                        <div class="card-action" style="color: var(--text-secondary);">
                            Kullanıma Kapalı <i data-lucide="lock" size="16"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. Öğretmen Sınav Analiz Görünümü -->
            <div class="analysis-section" id="teacher-analysis-view">
                
                <!-- MOBİL VE WEB ORTAK TABS -->
                
                <!-- TAB 1: KARNE DETAYLARI -->
                <div id="analysis-tab-karne" style="display: flex; flex-direction: column; gap: 2rem; width:100%;">
                    <!-- Arama Bölümü -->
                    <div style="display: flex; gap: 0.75rem; align-items: center; width: 100%; position: relative; z-index: 50;">
                        <button class="btn btn-secondary" onclick="showTeacherHub()" style="padding: 0 1.25rem; border-radius: var(--radius-lg); height: 52px; display: inline-flex; align-items: center; justify-content: center; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); background: var(--bg-card); color: var(--text-primary);" title="Geri Dön">
                            <i data-lucide="arrow-left"></i> <span>Geri</span>
                        </button>
                        <div class="search-container" style="flex-grow: 1; position: relative;">
                            <div class="search-box-wrapper">
                                <i data-lucide="search" class="search-icon"></i>
                                <input type="text" class="search-input" id="search-student" placeholder="Öğrenci Adı veya Numarası ile Arayın..." autocomplete="off" style="height: 52px; border-radius: var(--radius-lg);">
                            </div>
                            <div class="search-results" id="search-results-list"></div>
                        </div>
                    </div>

                    <!-- Rapor ve Karne Gösterimi -->
                    <div class="info-card" id="student-report-card" style="display:none;">
                        <div class="info-card-header">
                            <div class="student-details">
                                <h2 id="report-student-name">MERYEM DAĞI</h2>
                                <div class="student-meta">
                                    <span class="badge badge-accent" id="report-student-no">No: 136</span>
                                    <span class="badge" id="report-student-class">Sınıf: 12</span>
                                    <span class="badge" id="report-student-branch">Şube: A</span>
                                    <span class="badge" id="report-student-exam-count">Deneme Sayısı: 0</span>
                                </div>
                            </div>
                            <button class="btn btn-primary" onclick="window.print()">
                                <i data-lucide="printer"></i> <span>Karne Yazdır / PDF Kaydet</span>
                            </button>
                        </div>

                        <!-- Sonuç Tablosu -->
                        <div class="table-container">
                            <table id="results-table">
                                <thead>
                                    <tr>
                                        <th rowspan="2" style="vertical-align: middle;">Deneme Sınav Adı</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Türkçe</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Sosyal</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Matematik</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Geometri</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Fizik</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Kimya</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Biyoloji</th>
                                        <th colspan="4" style="text-align:center; border-bottom: 1px solid var(--border-color);">Genel Toplam</th>
                                        <th rowspan="2" style="vertical-align: middle; text-align:center;">Puan</th>
                                        <th rowspan="2" style="vertical-align: middle; text-align:center;">Sıra</th>
                                    </tr>
                                    <tr class="subheader-row">
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                        <th>D</th><th>Y</th><th>B</th><th class="cell-net-header">N</th>
                                    </tr>
                                </thead>
                                <tbody id="results-table-body">
                                    <!-- JS ile doldurulacak -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Hoş Geldiniz Paneli -->
                    <div class="info-card" id="welcome-panel-analysis" style="text-align: center; padding: 4rem 2rem;">
                        <i data-lucide="activity" size="64" style="color:var(--accent-color); margin: 0 auto 1.5rem auto;"></i>
                        <h2 style="font-size: 1.75rem; font-weight:700; margin-bottom: 0.5rem;">Analiz Sistemine Hoş Geldiniz</h2>
                        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 2rem auto; font-size:0.95rem;">
                            Öğrenci karnelerini, sınav ortalamalarını ve net gelişim grafiklerini görmek için yukarıdaki arama kutusuna bir öğrencinin ismini veya numarasını yazarak arayınız.
                        </p>
                    </div>
                </div>

                <!-- TAB 2: GRAFIK GELISIMI (Desktop shows this inside the report automatically) -->
                <div id="analysis-tab-grafik" class="charts-container" style="width:100%;">
                    <div class="chart-card">
                        <h3>
                            <span><i data-lucide="trending-up" style="display:inline; vertical-align:-3px; margin-right:4px;"></i> Net Gelişim Grafiği</span>
                            <span style="font-size:0.75rem; font-weight:normal; color:var(--text-secondary);">Mavi: Öğrenci | Kırmızı: Okul Ortalaması</span>
                        </h3>
                        <div class="chart-wrapper">
                            <canvas id="progressChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: ISTATISTIKLER (Mobile Only View, Desktop displays in sidebar) -->
                <div id="analysis-tab-istatistik" class="mobile-only" style="width: 100%;">
                    <div class="info-card">
                        <h3 style="font-size:1.1rem; font-weight:700; border-bottom:1px solid var(--border-color); padding-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem;">
                            <i data-lucide="bar-chart-2" style="color:var(--accent-color);"></i> Okul Genel İstatistikleri
                        </h3>
                        <div class="stats-grid" style="grid-template-columns: 1fr; gap: 1rem; margin-top: 1rem;">
                            <div class="stat-card-small">
                                <span class="val" id="stat-students-mobile">0</span>
                                <span class="lbl">Kayıtlı Öğrenci</span>
                            </div>
                            <div class="stat-card-small">
                                <span class="val" id="stat-exams-mobile">0</span>
                                <span class="lbl">Toplam Deneme</span>
                            </div>
                            <div class="stat-card-small">
                                <span class="val" id="stat-avg-net-mobile">0.00</span>
                                <span class="lbl">Okul Genel Net Ortalaması</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 4: YONETIM VE AYARLAR (Mobile Only View, Desktop displays in sidebar) -->
                <div id="analysis-tab-ayarlar" class="mobile-only" style="width: 100%;">
                    <div class="info-card" style="gap: 1.5rem;">
                        <h3 style="font-size:1.1rem; font-weight:700; border-bottom:1px solid var(--border-color); padding-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem;">
                            <i data-lucide="settings" style="color:var(--accent-color);"></i> Veritabanı ve Sınav Yönetimi
                        </h3>
                        
                        <!-- Sınav Yükleme Mobile -->
                        <div style="display:flex; flex-direction:column; gap:0.75rem;">
                            <span style="font-size:0.875rem; font-weight:600; color:var(--text-secondary);">Yeni Sınav İçe Aktar (.xlsx/.xlsm)</span>
                            <div class="dropzone" onclick="document.getElementById('excel-file-input-mobile').click()">
                                <i data-lucide="file-spreadsheet" size="28" style="color:var(--accent-color);"></i>
                                <strong style="font-size:0.85rem;">Excel Dosyası Seçin</strong>
                                <p style="font-size:0.7rem;">Sınav Excel'ini seçmek için buraya dokunun</p>
                                <input type="file" id="excel-file-input-mobile" accept=".xlsx,.xlsm" onchange="handleExcelImport(event)">
                            </div>
                        </div>

                        <!-- Veritabanı Sıfırlama Mobile -->
                        <div style="display:flex; flex-direction:column; gap:0.75rem; border-top:1px solid var(--border-color); padding-top:1.5rem;">
                            <span style="font-size:0.875rem; font-weight:600; color:var(--text-secondary);">Sistem Sıfırlama</span>
                            <button class="btn btn-secondary" style="width:100%; border-color:#ef4444; color:#ef4444; justify-content:center; height: 44px;" onclick="resetToDefault()">
                                <i data-lucide="rotate-ccw"></i> Fabrika Ayarlarına Dön
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </main>
    </div>

    <!-- Password Modal -->
    <div class="modal" id="login-modal">
        <div class="modal-card">
            <div class="modal-header">
                <h3>Öğretmen Girişi</h3>
                <button class="close-btn" onclick="closeLoginModal()"><i data-lucide="x"></i></button>
            </div>
            <p style="font-size: 0.85rem; color:var(--text-secondary); font-weight:500;">
                Yönetici uygulamalarına erişebilmek için lütfen öğretmen giriş şifresini yazın.
            </p>
            <div class="input-group">
                <label for="password-input">Giriş Şifresi</label>
                <input type="password" id="password-input" class="input-field" placeholder="••••••••" onkeydown="handlePasswordKeydown(event)">
                <span class="error-message" id="login-error">Hatalı şifre! Lütfen tekrar deneyin.</span>
            </div>
            <button class="btn btn-primary" style="justify-content:center;" onclick="verifyPassword()">Giriş Yap</button>
        </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast toast-success" id="status-toast">
        <i data-lucide="check-circle" size="18"></i>
        <span id="toast-message">Başarıyla tamamlandı!</span>
    </div>

    <!-- MOBILE BOTTOM NAVIGATION BARS (MEB e-Okul Mobil Style) -->
    
    <!-- 1. Portal Screen Bottom Bar (Ana Sayfa & Duyurular) -->
    <div class="mobile-nav-bar" id="mobile-nav-portal">
        <button class="mobile-nav-item active" id="nav-portal-home" onclick="switchPortalTab('home')">
            <i data-lucide="home"></i>
            <span>Girişler</span>
        </button>
        <button class="mobile-nav-item" id="nav-portal-announcements" onclick="switchPortalTab('announcements')">
            <i data-lucide="megaphone"></i>
            <span>Duyurular</span>
        </button>
    </div>

    <!-- 2. Teacher Analysis Dashboard Bottom Bar (Karne, Grafik, İstatistik, Yönetim) -->
    <div class="mobile-nav-bar" id="mobile-nav-analysis" style="display:none;">
        <button class="mobile-nav-item active" id="nav-analysis-karne" onclick="switchAnalysisTab('karne')">
            <i data-lucide="clipboard-list"></i>
            <span>Karne</span>
        </button>
        <button class="mobile-nav-item" id="nav-analysis-grafik" onclick="switchAnalysisTab('grafik')">
            <i data-lucide="trending-up"></i>
            <span>Grafik</span>
        </button>
        <button class="mobile-nav-item" id="nav-analysis-istatistik" onclick="switchAnalysisTab('istatistik')">
            <i data-lucide="bar-chart-2"></i>
            <span>İstatistik</span>
        </button>
        <button class="mobile-nav-item" id="nav-analysis-ayarlar" onclick="switchAnalysisTab('ayarlar')">
            <i data-lucide="settings"></i>
            <span>Yönetim</span>
        </button>
    </div>

    <footer>
        &copy; 2026 Ceylanpınar Fen Lisesi. Tüm Hakları Saklıdır.
    </footer>

    <script>
        // Default dataset embedded from Python extraction
        const DEFAULT_DATA = /* DATABASE_PLACEHOLDER */;

        let db = null;
        let examDatabase = [];
        let activeStudent = null;
        let progressChart = null;

        // Initialize App
        window.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            initTheme();
            initIndexedDB();
            initSearch();
            setupDragAndDrop();
            checkSession();
        });

        // Theme management
        function initTheme() {
            const currentTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', currentTheme);
            updateThemeButtonIcon(currentTheme);
        }

        function toggleTheme() {
            const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateThemeButtonIcon(theme);
            if (activeStudent) {
                renderProgressChart(activeStudent); // redraw chart with new colors
            }
        }

        function updateThemeButtonIcon(theme) {
            const btn = document.getElementById('theme-btn');
            if (theme === 'dark') {
                btn.innerHTML = '<i data-lucide="sun"></i>';
            } else {
                btn.innerHTML = '<i data-lucide="moon"></i>';
            }
            lucide.createIcons({ attrs: { class: 'lucide' } });
        }

        // Login Logic
        function openLoginModal() {
            document.getElementById('login-modal').classList.add('open');
            document.getElementById('password-input').focus();
            document.getElementById('login-error').style.display = 'none';
        }

        function closeLoginModal() {
            document.getElementById('login-modal').classList.remove('open');
            document.getElementById('password-input').value = '';
        }

        // e-Okul Mobile Bottom Nav Controller: Portal Selection View
        function switchPortalTab(tabName) {
            document.querySelectorAll('#mobile-nav-portal .mobile-nav-item').forEach(item => item.classList.remove('active'));
            
            if (tabName === 'home') {
                document.getElementById('nav-portal-home').classList.add('active');
                document.getElementById('portal-tab-home').style.display = 'flex';
                document.getElementById('portal-tab-announcements').style.setProperty('display', '', 'important'); // default desktop styling
                // In mobile, we want to hide announcements if we are on home tab
                if (window.innerWidth <= 768) {
                    document.getElementById('portal-tab-announcements').style.setProperty('display', 'none', 'important');
                }
            } else if (tabName === 'announcements') {
                document.getElementById('nav-portal-announcements').classList.add('active');
                document.getElementById('portal-tab-home').style.setProperty('display', 'none', 'important');
                document.getElementById('portal-tab-announcements').style.setProperty('display', 'flex', 'important');
            }
            lucide.createIcons();
        }

        // e-Okul Mobile Bottom Nav Controller: Teacher Analysis View
        function switchAnalysisTab(tabName) {
            document.querySelectorAll('#mobile-nav-analysis .mobile-nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById(`nav-analysis-${tabName}`).classList.add('active');

            // Hide all sub-tabs
            document.getElementById('analysis-tab-karne').style.setProperty('display', 'none', 'important');
            document.getElementById('analysis-tab-grafik').style.setProperty('display', 'none', 'important');
            document.getElementById('analysis-tab-istatistik').style.setProperty('display', 'none', 'important');
            document.getElementById('analysis-tab-ayarlar').style.setProperty('display', 'none', 'important');

            // Show selected sub-tab
            if (tabName === 'karne') {
                document.getElementById('analysis-tab-karne').style.setProperty('display', 'flex', 'important');
            } else if (tabName === 'grafik') {
                document.getElementById('analysis-tab-grafik').style.setProperty('display', 'flex', 'important');
                if (activeStudent) {
                    setTimeout(() => renderProgressChart(activeStudent), 50); // delay to let canvas layout settle
                }
            } else if (tabName === 'istatistik') {
                document.getElementById('analysis-tab-istatistik').style.setProperty('display', 'block', 'important');
            } else if (tabName === 'ayarlar') {
                document.getElementById('analysis-tab-ayarlar').style.setProperty('display', 'block', 'important');
            }
            lucide.createIcons();
        }

        // Responsive resize handler to reset layout displaying rules
        window.addEventListener('resize', () => {
            const isMobile = window.innerWidth <= 768;
            
            // Adjust portal grid displays
            if (!isMobile) {
                document.getElementById('portal-tab-home').style.display = 'flex';
                document.getElementById('portal-tab-announcements').style.display = 'flex';
                
                // On desktop, show all analysis tabs
                document.getElementById('analysis-tab-karne').style.display = 'flex';
                document.getElementById('analysis-tab-grafik').style.display = 'block';
                document.getElementById('analysis-tab-istatistik').style.display = 'none';
                document.getElementById('analysis-tab-ayarlar').style.display = 'none';
            } else {
                // If resized back to mobile, maintain active tabs
                if (document.getElementById('selection-screen').style.display !== 'none') {
                    const activePortalTab = document.querySelector('#mobile-nav-portal .mobile-nav-item.active').id;
                    if (activePortalTab === 'nav-portal-home') {
                        switchPortalTab('home');
                    } else {
                        switchPortalTab('announcements');
                    }
                } else if (document.getElementById('teacher-analysis-view').style.display !== 'none') {
                    const activeAnalysisTab = document.querySelector('#mobile-nav-analysis .mobile-nav-item.active').id.replace('nav-analysis-', '');
                    switchAnalysisTab(activeAnalysisTab);
                }
            }
        });

        function handlePasswordKeydown(event) {
            if (event.key === 'Enter') {
                verifyPassword();
            }
        }

        function verifyPassword() {
            const passwordVal = document.getElementById('password-input').value;
            // Default password is set to ceylanpinar2014
            if (passwordVal === 'ceylanpinar2014') {
                sessionStorage.setItem('teacher_logged_in', 'true');
                closeLoginModal();
                showTeacherHub();
            } else {
                document.getElementById('login-error').style.display = 'block';
                document.getElementById('password-input').value = '';
                document.getElementById('password-input').focus();
            }
        }

        // Screen Routing
        function showSelectionScreen() {
            document.getElementById('app-container').classList.add('no-sidebar');
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('selection-screen').style.display = 'grid';
            document.getElementById('logout-btn').style.display = 'none';
            document.getElementById('header-subtitle').innerText = 'Portal Hub';
            
            // Mobile Nav bars
            document.getElementById('mobile-nav-portal').style.display = ''; // let CSS override (flex in mobile, none in desktop)
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
            
            if (window.innerWidth <= 768) {
                switchPortalTab('home');
            }
        }

        function showStudentHub() {
            document.getElementById('app-container').classList.add('no-sidebar');
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('student-hub').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-subtitle').innerText = 'Öğrenci Portalı';
            
            // Hide portal bottom bar since student hub has no tabs yet
            document.getElementById('mobile-nav-portal').style.setProperty('display', 'none', 'important');
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
        }

        function showTeacherHub() {
            document.getElementById('app-container').classList.add('no-sidebar');
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'block';
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-subtitle').innerText = 'Öğretmen Portalı';
            
            // Hide portal bottom bar
            document.getElementById('mobile-nav-portal').style.setProperty('display', 'none', 'important');
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
        }

        function showTeacherAnalysisView() {
            document.getElementById('app-container').classList.remove('no-sidebar');
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'flex';
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-subtitle').innerText = 'Deneme Analiz Sistemi';
            
            // Mobile Nav bars
            document.getElementById('mobile-nav-portal').style.setProperty('display', 'none', 'important');
            document.getElementById('mobile-nav-analysis').style.display = ''; // let CSS override (flex in mobile, none in desktop)
            
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                switchAnalysisTab('karne');
            } else {
                // On desktop, show karne & graphic, hide mobile-only tabs
                document.getElementById('analysis-tab-karne').style.display = 'flex';
                document.getElementById('analysis-tab-grafik').style.display = 'block';
                document.getElementById('analysis-tab-istatistik').style.display = 'none';
                document.getElementById('analysis-tab-ayarlar').style.display = 'none';
            }
            
            refreshDashboard();
        }

        function handleLogoClick() {
            if (sessionStorage.getItem('teacher_logged_in') === 'true') {
                showTeacherHub();
            } else if (document.getElementById('student-hub').style.display === 'block') {
                showStudentHub();
            } else {
                showSelectionScreen();
            }
        }

        function logout() {
            sessionStorage.removeItem('teacher_logged_in');
            showSelectionScreen();
        }

        function checkSession() {
            if (sessionStorage.getItem('teacher_logged_in') === 'true') {
                showTeacherHub();
            } else {
                showSelectionScreen();
            }
        }

        // IndexedDB Management
        function initIndexedDB() {
            const request = indexedDB.open('SchoolExamsDB', 1);

            request.onerror = (event) => {
                console.error("IndexedDB load error:", event);
                showToast("Veritabanı yüklenemedi, veriler geçici bellekten okunuyor.", "warning");
                examDatabase = DEFAULT_DATA;
                refreshDashboard();
            };

            request.onsuccess = (event) => {
                db = event.target.result;
                loadRecordsFromDB();
            };

            request.onupgradeneeded = (event) => {
                const database = event.target.result;
                const objectStore = database.createObjectStore("exams", { keyPath: "id", autoIncrement: true });
                objectStore.createIndex("no", "no", { unique: false });
                objectStore.createIndex("name", "name", { unique: false });
                objectStore.createIndex("deneme", "deneme", { unique: false });
            };
        }

        function loadRecordsFromDB() {
            const transaction = db.transaction(["exams"], "readonly");
            const objectStore = transaction.objectStore("exams");
            const request = objectStore.getAll();

            request.onsuccess = (event) => {
                const results = event.target.result;
                if (results.length === 0) {
                    console.log("Database is empty. Populating default records...");
                    populateDefaultData();
                } else {
                    examDatabase = results;
                    console.log(`Loaded ${results.length} records from IndexedDB`);
                    refreshDashboard();
                }
            };
        }

        function populateDefaultData() {
            const transaction = db.transaction(["exams"], "readwrite");
            const objectStore = transaction.objectStore("exams");
            
            DEFAULT_DATA.forEach(record => {
                objectStore.add(record);
            });

            transaction.oncomplete = () => {
                console.log("Default records written to IndexedDB.");
                examDatabase = DEFAULT_DATA;
                showToast("Varsayılan veritabanı (672 kayıt) başarıyla yüklendi.");
                refreshDashboard();
            };
        }

        function saveRecordsToDB(newRecords, message = "Veritabanı güncellendi") {
            if (!db) {
                examDatabase = [...examDatabase, ...newRecords];
                refreshDashboard();
                showToast(message);
                return;
            }

            const transaction = db.transaction(["exams"], "readwrite");
            const objectStore = transaction.objectStore("exams");

            newRecords.forEach(record => {
                objectStore.add(record);
            });

            transaction.oncomplete = () => {
                const reloadTransaction = db.transaction(["exams"], "readonly");
                const reloadStore = reloadTransaction.objectStore("exams");
                const request = reloadStore.getAll();
                
                request.onsuccess = (event) => {
                    examDatabase = event.target.result;
                    refreshDashboard();
                    showToast(message);
                };
            };
        }

        function resetToDefault() {
            if (!confirm("Tüm eklediğiniz sınav verilerini silip fabrika ayarlarına dönmek istediğinize emin misiniz?")) return;

            const transaction = db.transaction(["exams"], "readwrite");
            const objectStore = transaction.objectStore("exams");
            
            const clearRequest = objectStore.clear();
            clearRequest.onsuccess = () => {
                populateDefaultData();
                activeStudent = null;
                document.getElementById('student-report-card').style.display = 'none';
                document.getElementById('welcome-panel-analysis').style.display = 'block';
                document.getElementById('search-student').value = '';
            };
        }

        // Dashboard statistics
        function refreshDashboard() {
            const uniqueStudents = new Set();
            const uniqueExams = new Set();
            let totalNetSum = 0;
            let totalNetCount = 0;

            examDatabase.forEach(record => {
                uniqueStudents.add(record.no);
                uniqueExams.add(record.deneme);
                if (record.subjects && record.subjects.toplam) {
                    totalNetSum += record.subjects.toplam.n;
                    totalNetCount++;
                }
            });

            const totalStudentsCount = uniqueStudents.size;
            const totalExamsCount = uniqueExams.size;
            const schoolAvgNet = totalNetCount > 0 ? (totalNetSum / totalNetCount).toFixed(2) : "0.00";

            // Update Desktop Stats
            document.getElementById('stat-students').innerText = totalStudentsCount;
            document.getElementById('stat-exams').innerText = totalExamsCount;
            document.getElementById('stat-avg-net').innerText = schoolAvgNet;

            // Update Mobile Stats
            document.getElementById('stat-students-mobile').innerText = totalStudentsCount;
            document.getElementById('stat-exams-mobile').innerText = totalExamsCount;
            document.getElementById('stat-avg-net-mobile').innerText = schoolAvgNet;
        }

        // Search logic
        function initSearch() {
            const searchInput = document.getElementById('search-student');
            const resultsList = document.getElementById('search-results-list');

            searchInput.addEventListener('input', () => {
                const query = searchInput.value.toLowerCase().trim();
                if (query.length < 1) {
                    resultsList.style.display = 'none';
                    return;
                }

                const matchingStudents = [];
                const addedIds = new Set();

                examDatabase.forEach(r => {
                    const matchesName = r.name.toLowerCase().includes(query);
                    const matchesNo = String(r.no).includes(query);

                    if ((matchesName || matchesNo) && !addedIds.has(r.no)) {
                        addedIds.add(r.no);
                        matchingStudents.push({
                            no: r.no,
                            name: r.name,
                            class: r.class,
                            branch: r.branch
                        });
                    }
                });

                matchingStudents.sort((a, b) => a.name.localeCompare(b.name, 'tr'));

                if (matchingStudents.length === 0) {
                    resultsList.innerHTML = '<div class="search-result-item" style="color:var(--text-secondary); cursor:default;">Sonuç Bulunamadı</div>';
                } else {
                    resultsList.innerHTML = matchingStudents.map(student => `
                        <div class="search-result-item" onclick="selectStudent(${student.no})">
                            <span>${student.name}</span>
                            <span class="meta">No: ${student.no} | ${student.class}${student.branch}</span>
                        </div>
                    `).join('');
                }
                resultsList.style.display = 'block';
            });

            document.addEventListener('click', (e) => {
                if (!searchInput.contains(e.target) && !resultsList.contains(e.target)) {
                    resultsList.style.display = 'none';
                }
            });
        }

        function selectStudent(studentNo) {
            document.getElementById('search-results-list').style.display = 'none';
            document.getElementById('search-student').value = '';

            const studentRecords = examDatabase.filter(r => r.no === studentNo);
            if (studentRecords.length === 0) return;

            studentRecords.sort((a, b) => {
                const dateA = extractDate(a.deneme);
                const dateB = extractDate(b.deneme);
                return dateA - dateB;
            });

            activeStudent = studentRecords;
            displayStudentReport(studentRecords);
        }

        function extractDate(examName) {
            const match = examName.match(/(\\d{2})[\\/.-](\\d{2})[\\/.-](\\d{4})/);
            if (match) {
                return new Date(match[3], match[2] - 1, match[1]);
            }
            return new Date(0);
        }

        function displayStudentReport(records) {
            document.getElementById('welcome-panel-analysis').style.display = 'none';
            const card = document.getElementById('student-report-card');
            card.style.display = 'flex';

            const first = records[0];
            document.getElementById('report-student-name').innerText = first.name;
            document.getElementById('report-student-no').innerText = `No: ${first.no}`;
            document.getElementById('report-student-class').innerText = `Sınıf: ${first.class}`;
            document.getElementById('report-student-branch').innerText = first.branch ? `Şube: ${first.branch}` : 'Şube: -';
            document.getElementById('report-student-exam-count').innerText = `Deneme Sayısı: ${records.length}`;

            const tbody = document.getElementById('results-table-body');
            tbody.innerHTML = '';

            let sumNets = { turkce:0, sosyal:0, matematik:0, geometri:0, fizik:0, kimya:0, biyoloji:0, toplam:0 };

            records.forEach(r => {
                const sub = r.subjects || {};
                const t = sub.turkce || {d:0,y:0,b:0,n:0};
                const s = sub.sosyal || {d:0,y:0,b:0,n:0};
                const m = sub.matematik || {d:0,y:0,b:0,n:0};
                const g = sub.geometri || {d:0,y:0,b:0,n:0};
                const f = sub.fizik || {d:0,y:0,b:0,n:0};
                const k = sub.kimya || {d:0,y:0,b:0,n:0};
                const b = sub.biyoloji || {d:0,y:0,b:0,n:0};
                const tot = sub.toplam || {d:0,y:0,b:0,n:0};

                sumNets.turkce += t.n;
                sumNets.sosyal += s.n;
                sumNets.matematik += m.n;
                sumNets.geometri += g.n;
                sumNets.fizik += f.n;
                sumNets.kimya += k.n;
                sumNets.biyoloji += b.n;
                sumNets.toplam += tot.n;

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight: 600;">${r.deneme}</td>
                    <td style="text-align:center;">${t.d}</td><td style="text-align:center;">${t.y}</td><td style="text-align:center;">${t.b}</td><td class="cell-net">${t.n.toFixed(2)}</td>
                    <td style="text-align:center;">${s.d}</td><td style="text-align:center;">${s.y}</td><td style="text-align:center;">${s.b}</td><td class="cell-net">${s.n.toFixed(2)}</td>
                    <td style="text-align:center;">${m.d}</td><td style="text-align:center;">${m.y}</td><td style="text-align:center;">${m.b}</td><td class="cell-net">${m.n.toFixed(2)}</td>
                    <td style="text-align:center;">${g.d}</td><td style="text-align:center;">${g.y}</td><td style="text-align:center;">${g.b}</td><td class="cell-net">${g.n.toFixed(2)}</td>
                    <td style="text-align:center;">${f.d}</td><td style="text-align:center;">${f.y}</td><td style="text-align:center;">${f.b}</td><td class="cell-net">${f.n.toFixed(2)}</td>
                    <td style="text-align:center;">${k.d}</td><td style="text-align:center;">${k.y}</td><td style="text-align:center;">${k.b}</td><td class="cell-net">${k.n.toFixed(2)}</td>
                    <td style="text-align:center;">${b.d}</td><td style="text-align:center;">${b.y}</td><td style="text-align:center;">${b.b}</td><td class="cell-net">${b.n.toFixed(2)}</td>
                    <td style="text-align:center; font-weight:600;">${tot.d}</td><td style="text-align:center; font-weight:600;">${tot.y}</td><td style="text-align:center; font-weight:600;">${tot.b}</td><td class="cell-net">${tot.n.toFixed(2)}</td>
                    <td class="cell-score" style="text-align:center;">${r.puan > 0 ? r.puan.toFixed(3) : '-'}</td>
                    <td class="cell-rank" style="text-align:center;">${r.siralama > 0 ? r.siralama : '-'}</td>
                `;
                tbody.appendChild(tr);
            });

            const avgRow = document.createElement('tr');
            avgRow.className = 'total-row';
            const count = records.length;
            avgRow.innerHTML = `
                <td>ORTALAMALAR</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.turkce / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.sosyal / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.matematik / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.geometri / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.fizik / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.kimya / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.biyoloji / count).toFixed(2)}</td>
                <td colspan="3"></td><td class="cell-net">${(sumNets.toplam / count).toFixed(2)}</td>
                <td colspan="2"></td>
            `;
            tbody.appendChild(avgRow);

            // Redraw chart
            renderProgressChart(records);
            
            // If on mobile, switch to Karne tab to show results
            if (window.innerWidth <= 768) {
                switchAnalysisTab('karne');
            }
        }

        function renderProgressChart(records) {
            const canvasEl = document.getElementById('progressChart');
            if(!canvasEl) return;
            const ctx = canvasEl.getContext('2d');
            if (progressChart) {
                progressChart.destroy();
            }

            const labels = records.map(r => r.deneme.split(" ")[0]);
            const studentNets = records.map(r => r.subjects.toplam.n);

            const schoolAverages = records.map(r => {
                const examName = r.deneme;
                const examRecords = examDatabase.filter(rec => rec.deneme === examName);
                if (examRecords.length === 0) return 0;
                const netSum = examRecords.reduce((sum, rec) => sum + (rec.subjects.toplam.n || 0), 0);
                return Number((netSum / examRecords.length).toFixed(2));
            });

            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const gridColor = isDark ? '#334155' : '#e2e8f0';
            const textTextColor = isDark ? '#94a3b8' : '#64748b';

            progressChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Öğrencinin Toplam Neti',
                            data: studentNets,
                            borderColor: '#6366f1',
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            borderWidth: 3,
                            tension: 0.3,
                            fill: true,
                            pointBackgroundColor: '#6366f1',
                            pointRadius: 5
                        },
                        {
                            label: 'Okul Sınav Ortalaması',
                            data: schoolAverages,
                            borderColor: '#ef4444',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            tension: 0.1,
                            fill: false,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: textTextColor,
                                font: {
                                    family: 'Plus Jakarta Sans',
                                    weight: '600'
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: gridColor
                            },
                            ticks: {
                                color: textTextColor
                            }
                        },
                        y: {
                            grid: {
                                color: gridColor
                            },
                            ticks: {
                                color: textTextColor
                            },
                            min: 0,
                            max: 120
                        }
                    }
                }
            });
        }

        // Excel Drag and Drop
        function setupDragAndDrop() {
            const dropzone = document.getElementById('excel-dropzone');
            if(!dropzone) return;

            ['dragenter', 'dragover'].forEach(eventName => {
                dropzone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dropzone.classList.add('dragover');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropzone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dropzone.classList.remove('dragover');
                }, false);
            });

            dropzone.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files.length > 0) {
                    importExcelFile(files[0]);
                }
            });
        }

        function handleExcelImport(event) {
            const file = event.target.files[0];
            if (file) {
                importExcelFile(file);
            }
        }

        function importExcelFile(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    
                    const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                    if (rows.length < 3) {
                        showToast("Hata: Dosya formatı uyumsuz veya veri yok.", "error");
                        return;
                    }

                    const newRecords = [];
                    let importedExamName = "Bilinmeyen Deneme";

                    for(let i = 2; i < rows.length; i++) {
                        if (rows[i][38]) {
                            importedExamName = rows[i][38];
                            break;
                        }
                    }

                    for (let r = 2; r < rows.length; r++) {
                        const row = rows[r];
                        if (!row || row.length === 0) continue;

                        const rawNo = row[0];
                        const rawName = row[1];
                        if (!rawName || String(rawName).trim() === "") continue;

                        const no = rawNo ? parseInt(rawNo) : 0;
                        const name = String(rawName).trim();
                        const snf = row[2] ? String(row[2]).trim() : "";
                        const sube = row[3] ? String(row[3]).trim() : "";

                        const parseSubject = (startIdx) => {
                            const d = parseFloat(row[startIdx]) || 0;
                            const y = parseFloat(row[startIdx+1]) || 0;
                            const b = parseFloat(row[startIdx+2]) || 0;
                            const n = parseFloat(row[startIdx+3]) || parseFloat(d - (y / 4.0)) || 0;
                            return { d, y, b, n: Math.max(0, n) };
                        };

                        const subjects = {
                            turkce: parseSubject(4),
                            sosyal: parseSubject(8),
                            matematik: parseSubject(12),
                            geometri: parseSubject(16),
                            fizik: parseSubject(20),
                            kimya: parseSubject(24),
                            biyoloji: parseSubject(28),
                            toplam: parseSubject(32)
                        };

                        const puan = parseFloat(row[36]) || 0;
                        const siralama = parseInt(row[37]) || 0;
                        const deneme = row[38] ? String(row[38]).trim() : importedExamName;

                        newRecords.push({
                            no,
                            name,
                            class: snf,
                            branch: sube,
                            subjects,
                            puan,
                            siralama,
                            deneme
                        });
                    }

                    if (newRecords.length > 0) {
                        saveRecordsToDB(newRecords, `"${importedExamName}" sınavına ait ${newRecords.length} kayıt eklendi!`);
                    } else {
                        showToast("Dosyada geçerli öğrenci kaydı bulunamadı.", "error");
                    }

                } catch (error) {
                    console.error("Excel import error:", error);
                    showToast("Excel dosyası çözümlenirken hata oluştu.", "error");
                }
            };
            reader.readAsArrayBuffer(file);
        }

        // Backup Export / Import
        function exportData() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(examDatabase, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", `sinav_veri_tabani_yedek_${new Date().toISOString().slice(0,10)}.json`);
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
            showToast("Veri yedek dosyası (.json) bilgisayarınıza indirildi.");
        }

        function triggerImport() {
            document.getElementById('backup-file-input').click();
        }

        function importData(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const records = JSON.parse(e.target.result);
                    if (!Array.isArray(records)) {
                        showToast("Hata: Geçersiz yedek dosyası formatı.", "error");
                        return;
                    }

                    if (confirm(`Yedek dosyasındaki ${records.length} kaydı veritabanına eklemek istiyor musunuz?`)) {
                        saveRecordsToDB(records, "Yedek başarıyla yüklendi!");
                    }
                } catch (error) {
                    showToast("Hata: Dosya içeriği okunamadı.", "error");
                }
            };
            reader.readAsText(file);
        }

        // Toast notifications
        function showToast(message, type = "success") {
            const toast = document.getElementById('status-toast');
            if(!toast) return;
            const msgSpan = document.getElementById('toast-message');
            msgSpan.innerText = message;
            
            toast.className = "toast show";
            if (type === "error") {
                toast.style.borderLeft = "4px solid #ef4444";
            } else if (type === "warning") {
                toast.style.borderLeft = "4px solid #f59e0b";
            } else {
                toast.style.borderLeft = "4px solid var(--success-color)";
            }

            setTimeout(() => {
                toast.className = "toast";
            }, 3500);
        }
    </script>
</body>
</html>
"""
    
    # Perform replacement
    final_html = html_template.replace("/* DATABASE_PLACEHOLDER */", records_js_str)
    
    with open(html_out_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Merged web application HTML successfully compiled at: {html_out_path}")

if __name__ == "__main__":
    build_merged_app()
