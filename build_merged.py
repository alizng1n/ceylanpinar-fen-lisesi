import json
import os
import urllib.request
import re
import html

def fetch_live_news_python():
    target_url = "https://ceylanpinarfenlisesi.meb.k12.tr"
    print(f"Scraping live news in Python from: {target_url}")
    news_list = []
    try:
        req = urllib.request.Request(
            target_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            raw_body = response.read()
            try:
                html_content = raw_body.decode('utf-8')
            except UnicodeDecodeError:
                html_content = raw_body.decode('iso-8859-9', errors='ignore')
                
            html_content = html.unescape(html_content)
            news_matches = re.findall(r'<p class="alt_cizgi1"[^>]*>\s*<a href="(/icerikler/[^"]+)"[^>]*>(.*?)</a>', html_content, re.DOTALL)
            for href, title in news_matches:
                news_list.append({
                    'title': title.strip(),
                    'url': target_url + href.strip()
                })
        print(f"Successfully scraped {len(news_list)} news items in Python!")
    except Exception as e:
        print(f"Warning: Could not fetch live news in Python: {e}")
    return news_list

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

    # Okul Yonetim Sistemi veritabani (Cloud-Only yapısı için boş başlatılır, veriler sadece Supabase'den çekilir)
    okul_records = {"OkulAd": "CEYLANPINAR FEN LİSESİ", "idare": [], "ogretmen": [], "ogrenci": []}
    okul_js_str = json.dumps(okul_records, ensure_ascii=False)

    live_news = fetch_live_news_python()
    
    left_news_html = '<h3><i data-lucide="megaphone" size="20"></i> Haberler ve Duyurular</h3>'
    if live_news:
        left_items = live_news[:3]
        for idx, item in enumerate(left_items):
            ribbon = '<span class="ribbon">Yeni</span>' if idx == 0 else ''
            icon = 'bell' if idx == 0 else 'calendar'
            left_news_html += f"""
                        <a href="{item['url']}" target="_blank" class="news-card">
                            {ribbon}
                            <div class="news-icon-wrapper">
                                <i data-lucide="{icon}" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>{item['title']}</h4>
                                <p>Ceylanpınar Fen Lisesi resmi haber duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>"""
    else:
        left_news_html += """
                        <div class="news-card">
                            <span class="ribbon">Yeni</span>
                            <div class="news-icon-wrapper">
                                <i data-lucide="bell" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Deneme Analiz Sistemi Güncellendi</h4>
                                <p>Yeni arayüz ve e-Okul esintili mobil görünüm devreye alındı.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </div>
                        <div class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="calendar" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Yaz Dönemi Destekleme Kursları</h4>
                                <p>12. sınıflar için hazırlık ders programları yakında yayınlanacak.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </div>"""

    right_news_html = '<h3><i data-lucide="award" size="20"></i> Sınav ve Gelişim Duyuruları</h3>'
    if live_news and len(live_news) > 3:
        right_items = live_news[3:5]
        for item in right_items:
            right_news_html += f"""
                        <a href="{item['url']}" target="_blank" class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="file-text" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>{item['title']}</h4>
                                <p>Ceylanpınar Fen Lisesi resmi sınav ve gelişim duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>"""
    else:
        right_news_html += """
                        <div class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="file-text" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>YKS Tercih Danışmanlığı</h4>
                                <p>Rehberlik servisimiz tercih dönemi boyunca aktif hizmet verecektir.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </div>"""
    
    html_template = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFL</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ef4444' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3Cpath d='M12 8l4 2-4 2-4-2Z'/%3E%3Cpath d='M10 11v1.5c0 0.8 0.8 1.2 2 1.2s2-0.4 2-1.2v-1.5'/%3E%3Cpath d='M15.5 10.5v3'/%3E%3C/svg%3E">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Supabase JS Client -->
    <script src="https://unpkg.com/@supabase/supabase-js@2"></script>
    
    <!-- SheetJS for Excel Reading -->
    <script src="https://unpkg.com/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    
    <!-- Chart.js for beautiful graphs -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --accent-gradient: linear-gradient(135deg, #1e3c72, #2a5298);
            --accent-color: #1e3c72;
            --accent-hover: #162a50;
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
        }

        /* Tema geçiş hızı ve performansı için animasyonlar optimize edilmiştir */
        body {
            transition: background-color 0.1s ease, color 0.1s ease;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* DYNAMIC PORTAL BACKGROUND MODES (e-Okul Style) */
        body.portal-mode {
            background: linear-gradient(135deg, #e2e8f0, #cbd5e1) !important;
            color: #0f172a !important;
        }
        
        [data-theme="dark"] body.portal-mode {
            background: linear-gradient(135deg, #102a43, #243b53) !important;
            color: #ffffff !important;
        }
        
        body.portal-mode header {
            background: rgba(226, 232, 240, 0.85) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(15, 23, 42, 0.1) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        [data-theme="dark"] body.portal-mode header {
            background: rgba(16, 42, 67, 0.85) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        body.portal-mode header .logo-title {
            color: #0f172a !important;
        }
        
        [data-theme="dark"] body.portal-mode header .logo-title {
            color: #ffffff !important;
        }
        
        body.portal-mode header .logo-subtitle {
            color: #64748b !important;
        }
        
        [data-theme="dark"] body.portal-mode header .logo-subtitle {
            color: rgba(255, 255, 255, 0.75) !important;
        }
        
        /* Button overrides in dark portal mode */
        [data-theme="dark"] body.portal-mode .btn-secondary {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
        }

        [data-theme="dark"] body.portal-mode .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.18) !important;
        }
        
        [data-theme="dark"] body.portal-mode .theme-toggle {
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
        }
        
        [data-theme="dark"] body.portal-mode .theme-toggle:hover {
            background: rgba(255, 255, 255, 0.1) !important;
        }

        body.portal-mode footer {
            background: transparent !important;
            border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
            color: #64748b !important;
        }

        [data-theme="dark"] body.portal-mode footer {
            border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
            color: rgba(255, 255, 255, 0.6) !important;
        }

        /* Header Style */
        header {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            z-index: 9999;
            box-shadow: var(--shadow-sm);
            box-sizing: border-box;
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

        /* Fixed Alignment for Header Actions (Resolves theme btn movement) */
        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-left: auto; /* Guarantees theme button stays pushed to the right when logo is hidden */
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
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.2);
        }

        .btn-primary:hover {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(30, 60, 114, 0.3);
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
            margin-top: 70px;
            min-height: calc(100vh - 70px);
            box-sizing: border-box;
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
            border-color: #1e3c72;
            background: rgba(30, 60, 114, 0.03);
        }

        .dropzone-icon {
            color: #1e3c72;
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

        /* Selection Screen (Duyurular altta olacak) */
        .portal-selection {
            display: flex;
            flex-direction: column;
            gap: 3.5rem;
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
            text-align: center;
        }

        .welcome-logo {
            width: 90px;
            height: 90px;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.12));
        }

        .portal-category {
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            font-weight: 700;
            color: #000000;
            margin-bottom: 0.1rem;
            opacity: 1;
        }

        [data-theme="dark"] .portal-category {
            color: #ffffff;
        }

        .portal-welcome h2 {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: #000000;
            margin: 0;
        }

        [data-theme="dark"] .portal-welcome h2 {
            color: #ffffff;
            background: none;
            -webkit-text-fill-color: initial;
        }

        .portal-welcome p {
            font-size: 1.05rem;
            font-weight: 500;
        }

        .selection-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }

        /* e-Okul MEB Style Split Card Buttons */
        .split-btn-card {
            display: flex;
            background: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            height: 90px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            text-decoration: none;
            color: #0f172a !important;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .split-btn-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.22);
        }

        .pane-color {
            width: 95px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            flex-shrink: 0;
        }

        .pane-color-teacher {
            background-color: #f07865; /* Coral / Salmon color */
        }

        .pane-color-student {
            background-color: #4fd1c5; /* Turquoise color */
        }

        .pane-text {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 1.5rem;
            text-align: left;
            background: #ffffff;
        }

        .pane-text h3 {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e293b;
        }
        
        .pane-text p {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 0.15rem;
            font-weight: 500;
        }

        /* Two-Column Announcements Layout at the bottom */
        .portal-announcements-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2.5rem;
            width: 100%;
        }

        .portal-announcements-grid h3 {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid rgba(15, 23, 42, 0.08) !important;
            padding-bottom: 0.5rem;
            color: #0f172a;
        }

        [data-theme="dark"] .portal-announcements-grid h3 {
            color: #ffffff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
        }

        /* MEB Style News/Announcement Cards */
        .news-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 1.25rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
            position: relative;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            color: #0f172a !important;
            text-decoration: none;
            border: 1px solid #e2e8f0;
        }

        .news-card:hover {
            transform: translateX(6px);
            border-color: #1e3c72;
            box-shadow: 0 10px 22 rgba(0,0,0,0.1);
        }

        .news-icon-wrapper {
            width: 48px;
            height: 48px;
            background: rgba(30, 60, 114, 0.05);
            color: #1e3c72;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .news-content {
            flex-grow: 1;
        }

        .news-content h4 {
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: #1e293b;
        }

        .news-content p {
            font-size: 0.8rem;
            color: #64748b;
            line-height: 1.4;
            font-weight: 500;
        }

        .news-arrow {
            color: #94a3b8;
            flex-shrink: 0;
        }

        /* e-Okul "Yeni" (New) Ribbon Style */
        .ribbon {
            position: absolute;
            top: 0;
            left: 0;
            background: #ef4444;
            color: #ffffff;
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.15rem 0.6rem;
            border-bottom-right-radius: 8px;
            border-top-left-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
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
        .portal-card-disabled .card-action {
            color: var(--text-secondary) !important;
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

        /* Redesigned Footer (Legible colors under light theme) */
        footer {
            background: transparent !important;
            border-top: 1px solid rgba(15, 23, 42, 0.08) !important;
            padding: 2.5rem 2rem;
            width: 100%;
            margin-top: auto;
        }

        [data-theme="dark"] body.portal-mode footer {
            border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            max-width: 1100px;
            margin: 0 auto;
            text-align: left;
        }

        .footer-col {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .footer-col h4 {
            font-size: 0.95rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #0f172a !important; /* Legible dark color in light mode */
        }

        [data-theme="dark"] body.portal-mode .footer-col h4 {
            color: #ffffff !important; /* White in dark mode */
        }

        [data-theme="dark"] .footer-col h4 {
            color: #ffffff !important;
        }

        .footer-col p, .footer-col a {
            font-size: 0.85rem;
            color: #475569 !important; /* Legible slate in light mode */
            line-height: 1.5;
            font-weight: 500;
            text-decoration: none;
        }

        [data-theme="dark"] body.portal-mode .footer-col p,
        [data-theme="dark"] body.portal-mode .footer-col a {
            color: rgba(255, 255, 255, 0.75) !important;
        }

        [data-theme="dark"] .footer-col p,
        [data-theme="dark"] .footer-col a {
            color: #94a3b8 !important;
        }

        /* Print CSS Styling */
        @media print {
            body.print-karne > *:not(#karne-print-area) {
                display: none !important;
            }
            #karne-print-area {
                display: block !important;
                position: absolute;
                top: 0; left: 0;
                width: 210mm;
                min-height: 297mm;
                background: #fff;
                color: #000;
                font-family: 'Inter', 'Outfit', sans-serif;
                font-size: 9pt;
                padding: 12mm 6mm;
                box-sizing: border-box;
            }
            #karne-print-area table {
                width: 100% !important;
                border-collapse: collapse !important;
                margin-top: 10px !important;
                margin-bottom: 10px !important;
            }
            #karne-print-area th, #karne-print-area td {
                border: 1px solid #000 !important;
                padding: 2.5px 1.5px !important;
                font-size: 7pt !important;
                text-align: center !important;
                line-height: 1.1 !important;
            }
            #karne-print-area th {
                background-color: #f3f4f6 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            #karne-print-area td:first-child,
            #karne-print-area th:first-child {
                text-align: left !important;
                padding-left: 4px !important;
                max-width: 120px !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }
            body, html {
                background: white !important;
                color: black !important;
            }

            header, aside, .search-container, .btn, .header-actions, .theme-toggle, .dropzone, .sidebar-card, .toast, .portal-selection, .hub-section, .mobile-nav-bar, footer {
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
                gap: 1.5rem;
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

            /* Slim down selection cards for mobile (Stacks Split Cards) */
            .selection-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .split-btn-card {
                height: 80px; /* Slimmer layout on mobile */
                border-radius: 12px;
            }

            .pane-color {
                width: 70px;
            }

            .pane-text {
                padding: 0 1rem;
            }

            .pane-text h3 {
                font-size: 0.95rem;
            }

            .pane-text p {
                font-size: 0.7rem;
            }

            .portal-selection {
                gap: 2.5rem;
            }

            .portal-welcome h2 {
                font-size: 1.75rem;
            }

            .portal-welcome p {
                font-size: 0.9rem;
            }

            .portal-announcements-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
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
            .news-card {
                padding: 1rem;
                gap: 0.75rem;
                border-radius: var(--radius-md);
            }

            .news-icon-wrapper {
                width: 40px;
                height: 40px;
            }

            .news-content h4 {
                font-size: 0.875rem;
            }

            .news-content p {
                font-size: 0.75rem;
            }
            
            /* Footer mobile layout */
            footer {
                padding: 2rem 1rem;
            }
            .footer-content {
                grid-template-columns: 1fr;
                gap: 1.5rem;
                text-align: center;
            }
            .footer-col {
                text-align: center;
                align-items: center;
            }
            .footer-col h4 {
                justify-content: center;
            }
        }

        /* Yazdirma ve Resmi Belge Sablon Stilleri */
        #print-section {
            display: none;
        }

        @media print {
            body.print-doc > *:not(#print-section) {
                display: none !important;
            }
            body {
                background: #fff !important;
                color: #000 !important;
            }
            #print-section {
                display: block !important;
                position: relative;
                width: 100%;
                margin: 0;
                padding: 0;
            }
            @page {
                size: A4 portrait;
                margin: 0;
            }
            .school-doc-paper.a6-paper {
                width: 105mm !important;
                height: 148mm !important;
                margin: 10mm !important;
                border: 3px solid #000 !important;
                box-sizing: border-box !important;
                page-break-inside: avoid;
            }
            .school-doc-paper.a4-paper {
                width: 210mm !important;
                margin: 10mm !important;
                border: none !important;
                box-sizing: border-box !important;
                page-break-inside: avoid;
            }
        }

        .school-doc-paper {
            background: #fff;
            color: #000;
            font-family: 'Verdana', sans-serif;
            padding: 1.5rem;
            border: 1px solid #000;
            border-radius: 4px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .school-doc-paper.a6-paper {
            width: 105mm;
            height: 148mm;
            padding: 8mm 6mm;
            border: 3px solid #000;
            border-radius: 0;
            box-shadow: none;
            box-sizing: border-box;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .school-doc-paper.a4-paper {
            width: 210mm;
            max-width: 100%;
            box-shadow: none;
            border: none;
            margin: 0;
            box-sizing: border-box;
        }
        .school-doc-header {
            text-align: center;
            border-bottom: 2px double #000;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        .school-doc-header h2 {
            font-size: 1.05rem;
            font-weight: bold;
            margin: 0 0 0.2rem 0;
            text-transform: uppercase;
        }
        .school-doc-header p {
            font-size: 0.8rem;
            margin: 0;
            font-weight: 600;
        }
        .school-doc-title {
            text-align: center;
            font-size: 0.9rem;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }
        .school-doc-body {
            font-size: 0.82rem;
            line-height: 1.5;
            text-align: justify;
            margin-bottom: 1.5rem;
        }
        .school-doc-details {
            display: grid;
            grid-template-columns: 140px 1fr;
            gap: 0.3rem;
            margin-bottom: 1rem;
            font-size: 0.8rem;
        }
        .school-doc-details-label {
            font-weight: bold;
        }
        .school-doc-footer {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-top: 2rem;
            font-size: 0.8rem;
        }
        .school-doc-signature {
            text-align: center;
            min-width: 150px;
        }
        .school-doc-signature-title {
            font-weight: bold;
            margin-bottom: 2rem;
        }
            .btn-action {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            border: none;
            border-radius: 6px;
            padding: 0.25rem 0.55rem;
            font-size: 0.76rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Inter', sans-serif;
            outline: none;
        }
        .btn-action svg {
            width: 12px !important;
            height: 12px !important;
            stroke-width: 2.5px !important;
        }
        .btn-action:not(:last-child) {
            margin-right: 0.35rem;
        }
        .btn-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }
        .btn-action:active {
            transform: translateY(0);
        }

        /* Belge Üret */
        .btn-action-print {
            background-color: rgba(16, 185, 129, 0.08);
            color: #059669;
        }
        .btn-action-print:hover {
            background-color: #10b981;
            color: #ffffff;
        }
        [data-theme="dark"] .btn-action-print {
            background-color: rgba(52, 211, 153, 0.15);
            color: #34d399;
        }
        [data-theme="dark"] .btn-action-print:hover {
            background-color: #34d399;
            color: #0c0a09;
        }

        /* İsimsiz Belge Üret */
        .btn-action-anon {
            background-color: rgba(245, 158, 11, 0.08);
            color: #d97706;
        }
        .btn-action-anon:hover {
            background-color: #f59e0b;
            color: #ffffff;
        }
        [data-theme="dark"] .btn-action-anon {
            background-color: rgba(251, 191, 36, 0.15);
            color: #fbbf24;
        }
        [data-theme="dark"] .btn-action-anon:hover {
            background-color: #fbbf24;
            color: #0c0a09;
        }

        /* Düzenle */
        .btn-action-edit {
            background-color: rgba(59, 130, 246, 0.08);
            color: #2563eb;
        }
        .btn-action-edit:hover {
            background-color: #3b82f6;
            color: #ffffff;
        }
        [data-theme="dark"] .btn-action-edit {
            background-color: rgba(96, 165, 250, 0.15);
            color: #60a5fa;
        }
        [data-theme="dark"] .btn-action-edit:hover {
            background-color: #60a5fa;
            color: #0c0a09;
        }

        /* Sil */
        .btn-action-delete {
            background-color: rgba(239, 68, 68, 0.08);
            color: #dc2626;
        }
        .btn-action-delete:hover {
            background-color: #ef4444;
            color: #ffffff;
        }
        [data-theme="dark"] .btn-action-delete {
            background-color: rgba(248, 113, 113, 0.15);
            color: #f87171;
        }
        [data-theme="dark"] .btn-action-delete:hover {
            background-color: #f87171;
            color: #ffffff;
        }

        .disable-transitions,
        .disable-transitions * {
            transition: none !important;
            animation: none !important;
        }

        .btn-action svg,
        .btn-action .lucide {
            width: 11px !important;
            height: 11px !important;
            stroke-width: 2.5px !important;
        }

        /* Arama kutusu boşken çarpı butonunu otomatik olarak gizle */
        .search-input:placeholder-shown ~ .clear-search-btn {
            display: none !important;
        }

        .school-table-row {
            border-bottom: 1px solid var(--border-color);
            transition: background-color 0.15s ease;
        }
        .school-table-row:hover {
            background-color: var(--bg-page) !important;
        }
    </style>
</head>
<body class="portal-mode">

    <header>
        <!-- Id and default hidden logo for selection page header -->
        <div class="logo-section" id="header-logo-section" style="display:none;" onclick="handleLogoClick()">
            <div class="logo-icon" id="logo-container">
                <img id="logo-img" class="logo-img" src="logo.png" alt="Logo">
            </div>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h1 class="logo-title" id="header-title">Ceylanpınar Fen Lisesi</h1>
                <p class="logo-subtitle" id="header-subtitle">Portal Hub</p>
            </div>
        </div>
        <div class="header-actions">
            <!-- Veritabanı Bağlantı Durum Rozeti -->
            <div id="db-status-badge" style="width:32px; height:32px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; background:rgba(100,116,139,0.08); border: 1px solid rgba(100,116,139,0.15); transition: all 0.2s ease;" title="Veritabanı: Bağlanıyor...">
                <span id="db-status-dot" style="width:8px; height:8px; border-radius:50%; background:#64748b; display:inline-block; transition: all 0.2s ease;"></span>
            </div>
            
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
            <div class="sidebar-card" id="sidebar-upload-card">
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
                <div class="stat-card-single" style="text-align: center; padding: 1rem; background: var(--bg-page); border-radius: 8px; border: 1px solid var(--border-color); margin-top: 0.75rem;">
                    <span class="val" id="stat-avg-net" style="font-size: 2rem; font-weight: 800; color: var(--accent-color); display: block;">0.00</span>
                    <span class="lbl" style="font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-top: 0.25rem;">Okul Genel Net Ortalaması</span>
                </div>
            </div>

            <!-- Veri Yönetimi -->
            <div class="sidebar-card" id="sidebar-reset-card">
                <h3><i data-lucide="settings"></i> Sistem Ayarları</h3>
                <button class="btn btn-secondary" style="width:100%; border-color:#ef4444; color:#ef4444; height: 42px; justify-content: center;" onclick="resetToDefault()" title="Tüm verileri veritabanından kalıcı olarak siler">
                    <i data-lucide="trash-2"></i> Tümünü Temizle
                </button>
            </div>
        </aside>

        <main>
            <!-- 1. Seçim Ekranı (e-Okul Style Layout) -->
            <div class="portal-selection" id="selection-screen">
                
                <!-- Üst Kısım: Karşılama ve Giriş Butonları -->
                <div style="display: flex; flex-direction: column; gap: 2rem; width: 100%; align-items: center; text-align: center;">
                    <div class="portal-welcome">
                        <img class="welcome-logo" src="logo.png" alt="Okul Logosu">
                        <span class="portal-category">T.C. MİLLÎ EĞİTİM BAKANLIĞI</span>
                        <h2>Ceylanpınar Fen Lisesi</h2>
                    </div>

                    <div class="selection-grid">
                        <!-- Öğretmen Giriş Kartı (Icon on left, Symmetrical) -->
                        <div class="split-btn-card" onclick="openLoginModal()">
                            <div class="pane-color pane-color-teacher">
                                <i data-lucide="user-cog" size="28"></i>
                            </div>
                            <div class="pane-text">
                                <h3>Öğretmen Girişi</h3>
                                <p>Sınav analiz ve yönetim araçları</p>
                            </div>
                        </div>

                        <!-- Öğrenci Giriş Kartı (Icon on left, Symmetrical) -->
                        <div class="split-btn-card" onclick="navigate('student-hub')">
                            <div class="pane-color pane-color-student">
                                <i data-lucide="graduation-cap" size="28"></i>
                            </div>
                            <div class="pane-text">
                                <h3>Öğrenci Girişi</h3>
                                <p>Kişisel karne ve gelişim grafikleri</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Alt Kısım: Duyurular & Haberler (İki Sütunlu) -->
                <div class="portal-announcements-grid">
                    <!-- Sol Sütun: Haberler / Duyurular -->
                    <div id="left-news-list" style="display: flex; flex-direction: column; gap: 1rem; width: 100%;">
                        <h3><i data-lucide="megaphone" size="20"></i> Haberler ve Duyurular</h3>
                        <a href="https://ceylanpinarfenlisesi.meb.k12.tr/icerikler/öğrencilerimiz-gazzeye-bağış-yaptı_16780532.html" target="_blank" class="news-card">
                            <span class="ribbon">Yeni</span>
                            <div class="news-icon-wrapper">
                                <i data-lucide="bell" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Öğrencilerimiz Gazze'ye Bağış yaptı</h4>
                                <p>Ceylanpınar Fen Lisesi resmi haber duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                        <a href="https://ceylanpinarfenlisesi.meb.k12.tr/icerikler/afet-tatbikatı-başarıyla-gerçekleştirildi_16683329.html" target="_blank" class="news-card">
                            
                            <div class="news-icon-wrapper">
                                <i data-lucide="calendar" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Afet Tatbikatı Başarıyla Gerçekleştirildi.</h4>
                                <p>Ceylanpınar Fen Lisesi resmi haber duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                        <a href="https://ceylanpinarfenlisesi.meb.k12.tr/icerikler/motivasyon-semineri_16594914.html" target="_blank" class="news-card">
                            
                            <div class="news-icon-wrapper">
                                <i data-lucide="calendar" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Motivasyon semineri</h4>
                                <p>Ceylanpınar Fen Lisesi resmi haber duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                    </div>

                    <!-- Sağ Sütun: Sınav ve Genel Duyurular -->
                    <div id="right-news-list" style="display: flex; flex-direction: column; gap: 1rem; width: 100%;">
                        <h3><i data-lucide="award" size="20"></i> Sınav ve Gelişim Duyuruları</h3>
                        <a href="https://ceylanpinarfenlisesi.meb.k12.tr/icerikler/satranç-turnuvasi_16397754.html" target="_blank" class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="file-text" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>SATRANÇ TURNUVASI</h4>
                                <p>Ceylanpınar Fen Lisesi resmi sınav ve gelişim duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                        <a href="https://ceylanpinarfenlisesi.meb.k12.tr/icerikler/kutadgu-bilig_15749417.html" target="_blank" class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="file-text" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>Kutadgu Bilig</h4>
                                <p>Ceylanpınar Fen Lisesi resmi sınav ve gelişim duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
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
                    <div class="portal-card" onclick="navigate('teacher-analysis')">
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

                    <!-- Okul Yönetim Sistemi Kartı -->
                    <div class="portal-card" onclick="navigate('school-management')">
                        <div class="card-icon-wrapper">
                            <i data-lucide="database" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Okul Yönetim Sistemi <span class="badge">Aktif</span></h3>
                            <p>Okuldaki 560 öğrenciyi, 37 öğretmeni ve idari kadroyu listeleyin, arayın ve yeni kayıt ekleyip düzenleyin.</p>
                        </div>
                        <div class="card-action">
                            Sisteme Giriş Yap <i data-lucide="arrow-right" size="16"></i>
                        </div>
                    </div>

                    <!-- Program Kartı (Placeholder) -->
                    <div class="portal-card portal-card-disabled">
                        <div class="card-icon-wrapper">
                            <i data-lucide="calendar" size="24"></i>
                        </div>
                        <div class="card-content">
                            <h3>Ders Programı & Nöbetler <span class="badge badge-disabled">Yakında</span></h3>
                            <p>Haftalık ders programlarını, nöbet çizelgelerini ve öğretmen izin/yedek planhamalarını yönetin.</p>
                        </div>
                        <div class="card-action" >
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
                        <div class="card-action" >
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
                        <div class="card-action" >
                            Kullanıma Kapalı <i data-lucide="lock" size="16"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. Öğretmen Sınav Analiz Görünümü -->
            <div class="analysis-section" id="teacher-analysis-view">
                
                <!-- TAB 1: KARNE DETAYLARI -->
                <div id="analysis-tab-karne" style="display: flex; flex-direction: column; gap: 2rem; width:100%;">
                    <!-- Arama Bölümü -->
                    <div style="display: flex; gap: 0.75rem; align-items: center; width: 100%; position: relative; z-index: 50;">
                        <!-- Back button goes back in browser history -->
                        <button class="btn btn-secondary" onclick="goBack('teacher-hub')" style="padding: 0 1.25rem; border-radius: var(--radius-lg); height: 52px; display: inline-flex; align-items: center; justify-content: center; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); background: var(--bg-card); color: var(--text-primary);" title="Geri Dön">
                            <i data-lucide="arrow-left"></i> <span>Geri</span>
                        </button>
                        <div class="search-container" style="flex-grow: 1; position: relative;">
                            <div class="search-box-wrapper" style="position:relative;">
                                <i data-lucide="search" class="search-icon"></i>
                                <input type="text" class="search-input" id="search-student" placeholder="Öğrenci Adı veya Numarası ile Arayın..." autocomplete="off" style="height: 52px; border-radius: var(--radius-lg); padding-right:40px;">
                                <button class="clear-search-btn" id="clear-search-student" onclick="clearSearchInput('search-student')" style="display:none; position:absolute; right:12px; top:50%; transform:translateY(-50%); background:none; border:none; color:#ef4444; cursor:pointer; padding:0.25rem; align-items:center; justify-content:center; z-index: 5;"><i data-lucide="x-circle" size="18"></i></button>
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
                            <button class="btn btn-primary" onclick="printKarne()">
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

                <!-- TAB 2: GRAFIK GELISIMI -->
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

                <!-- TAB 3: ISTATISTIKLER (Mobile Only View) -->
                <div id="analysis-tab-istatistik" class="mobile-only" style="width: 100%;">
                    <div class="info-card">
                        <h3 style="font-size:1.1rem; font-weight:700; border-bottom:1px solid var(--border-color); padding-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem; color:#1e293b;">
                            <i data-lucide="bar-chart-2" style="color:#1e3c72;"></i> Okul Genel İstatistikleri
                        </h3>
                        <div class="stat-card-single" style="text-align: center; padding: 1.25rem; background: var(--bg-page); border-radius: 8px; border: 1px solid var(--border-color); margin-top: 1rem;">
                            <span class="val" id="stat-avg-net-mobile" style="font-size: 2.2rem; font-weight: 800; color: var(--accent-color); display: block;">0.00</span>
                            <span class="lbl" style="font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-top: 0.25rem;">Okul Genel Net Ortalaması</span>
                        </div>
                    </div>
                </div>

                <!-- TAB 4: YONETIM VE AYARLAR (Mobile Only View) -->
                <div id="analysis-tab-ayarlar" class="mobile-only" style="width: 100%;">
                    <div class="info-card" style="gap: 1.5rem;">
                        <h3 style="font-size:1.1rem; font-weight:700; border-bottom:1px solid var(--border-color); padding-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem; color:#1e293b;">
                            <i data-lucide="settings" style="color:#1e3c72;"></i> Veritabanı ve Sınav Yönetimi
                        </h3>
                        
                        <!-- Sınav Yükleme Mobile -->
                        <div id="mobile-upload-section" style="display:flex; flex-direction:column; gap:0.75rem;">
                            <span style="font-size:0.875rem; font-weight:600; color:var(--text-secondary);">Yeni Sınav İçe Aktar (.xlsx/.xlsm)</span>
                            <div class="dropzone" onclick="document.getElementById('excel-file-input-mobile').click()">
                                <i data-lucide="file-spreadsheet" size="28" style="color:#1e3c72;"></i>
                                <strong style="font-size:0.85rem; color:#1e3c72;">Excel Dosyası Seçin</strong>
                                <p style="font-size:0.7rem;">Sınav Excel'ini seçmek için buraya dokunun</p>
                                <input type="file" id="excel-file-input-mobile" accept=".xlsx,.xlsm" onchange="handleExcelImport(event)">
                            </div>
                        </div>

                        <!-- Veritabanı Sıfırlama Mobile -->
                        <div id="mobile-reset-section" style="display:flex; flex-direction:column; gap:0.75rem; border-top:1px solid var(--border-color); padding-top:1.5rem;">
                            <span style="font-size:0.875rem; font-weight:600; color:var(--text-secondary);">Sistem Sıfırlama</span>
                            <button class="btn btn-secondary" style="width:100%; border-color:#ef4444; color:#ef4444; justify-content:center; height: 44px;" onclick="resetToDefault()" title="Tüm verileri siler">
                                <i data-lucide="trash-2"></i> Tümünü Temizle
                            </button>
                        </div>
                    </div>
                </div>

            </div>
    <div id="school-management-view" style="display:none; width:100%; box-sizing:border-box; animation: fadeIn 0.4s ease;">
        <div style="max-width:920px; margin:0 auto;">

            <!-- Header -->
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap;">
                <button class="btn btn-secondary" onclick="goBack('teacher-hub')" style="padding:0 1.25rem; border-radius:var(--radius-lg); height:44px; display:inline-flex; align-items:center; gap:0.5rem; box-shadow:var(--shadow-sm); border:1px solid var(--border-color); background:var(--bg-card); color:var(--text-primary);">
                    <i data-lucide="arrow-left" size="16"></i> <span>Geri</span>
                </button>
                <div>
                    <h2 style="margin:0; font-size:1.4rem; color:var(--text-primary); font-weight:700;">Okul Yönetim Sistemi</h2>
                    <p style="margin:0; font-size:0.85rem; color:var(--text-secondary);">Ceylanpınar Fen Lisesi &middot; Kayıt Yönetimi</p>
                </div>
            </div>

            <!-- Stats Row -->
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:1.5rem;">
                <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:1.25rem; text-align:center; box-shadow:var(--shadow-sm); border:1px solid var(--border-color);">
                    <div id="school-stat-ogrenci" style="font-size:2rem; font-weight:700; color:var(--accent-color);">560</div>
                    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem; font-weight:500;">Öğrenci</div>
                </div>
                <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:1.25rem; text-align:center; box-shadow:var(--shadow-sm); border:1px solid var(--border-color);">
                    <div id="school-stat-ogretmen" style="font-size:2rem; font-weight:700; color:var(--accent-color);">37</div>
                    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem; font-weight:500;">Öğretmen</div>
                </div>
                <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:1.25rem; text-align:center; box-shadow:var(--shadow-sm); border:1px solid var(--border-color);">
                    <div id="school-stat-idare" style="font-size:2rem; font-weight:700; color:var(--accent-color);">6</div>
                    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem; font-weight:500;">İdareci</div>
                </div>
            </div>

            <!-- Tab Navigation -->
            <div style="display:flex; gap:0.5rem; margin-bottom:1rem; background:var(--bg-card); border-radius:var(--radius-lg); padding:0.4rem; box-shadow:var(--shadow-sm); border:1px solid var(--border-color);">
                <button id="school-tab-ogrenci" onclick="switchSchoolTab('ogrenci')" style="flex:1; padding:0.6rem; border-radius:var(--radius); border:none; font-weight:600; font-size:0.85rem; cursor:pointer; transition:all 0.2s; background:var(--accent-gradient); color:#fff;">
                    <i data-lucide="users" size="14" style="vertical-align:middle;"></i> Öğrenciler
                </button>
                <button id="school-tab-ogretmen" onclick="switchSchoolTab('ogretmen')" style="flex:1; padding:0.6rem; border-radius:var(--radius); border:none; font-weight:600; font-size:0.85rem; cursor:pointer; transition:all 0.2s; background:transparent; color:var(--text-secondary);">
                    <i data-lucide="user-check" size="14" style="vertical-align:middle;"></i> Öğretmenler
                </button>
                <button id="school-tab-idare" onclick="switchSchoolTab('idare')" style="flex:1; padding:0.6rem; border-radius:var(--radius); border:none; font-weight:600; font-size:0.85rem; cursor:pointer; transition:all 0.2s; background:transparent; color:var(--text-secondary);">
                    <i data-lucide="briefcase" size="14" style="vertical-align:middle;"></i> İdareciler
                </button>
            </div>

            <!-- Search + Add Toolbar -->
            <div style="display:flex; gap:0.75rem; margin-bottom:1rem; align-items:center;">
                <div class="search-box-wrapper" style="flex:1; position:relative;">
                    <i data-lucide="search" class="search-icon"></i>
                    <input type="text" id="school-search-input" class="search-input" placeholder="İsim, numara veya sınıf ile arayın..." oninput="handleSchoolSearchInput()" style="height:44px; border-radius:var(--radius-lg); padding-right:40px;">
                    <button class="clear-search-btn" id="clear-school-search" onclick="clearSearchInput('school-search-input')" style="display:none; position:absolute; right:12px; top:50%; transform:translateY(-50%); background:none; border:none; color:#ef4444; cursor:pointer; padding:0.25rem; align-items:center; justify-content:center; z-index: 5;"><i data-lucide="x-circle" size="18"></i></button>
                </div>
                <button id="school-add-btn" onclick="openSchoolModal(null)" style="padding:0 1.25rem; height:44px; border-radius:var(--radius-lg); background:var(--accent-gradient); color:#fff; border:none; font-weight:600; font-size:0.875rem; cursor:pointer; display:inline-flex; align-items:center; gap:0.4rem; white-space:nowrap; box-shadow:var(--shadow-sm);">
                    <i data-lucide="plus" size="16"></i> Yeni Ekle
                </button>
                <button id="school-settings-btn" onclick="openSupabaseSettingsModal()" style="padding:0; width:44px; height:44px; border-radius:var(--radius-lg); background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-color); cursor:pointer; display:inline-flex; align-items:center; justify-content:center; box-shadow:var(--shadow-sm);" title="Supabase Bağlantı Ayarları">
                    <i data-lucide="settings" size="18"></i>
                </button>
            </div>

            <!-- Table Container -->
            <div style="background:var(--bg-card); border-radius:var(--radius-lg); box-shadow:var(--shadow-sm); border:1px solid var(--border-color); overflow:hidden;">
                <div id="school-table-body" style="max-height:55vh; overflow-y:auto;"></div>
                <div id="school-table-footer" style="padding:0.75rem 1rem; border-top:1px solid var(--border-color); font-size:0.8rem; color:var(--text-secondary); background:var(--bg-page);"></div>
            </div>

        </div>
    </div>
        </main>
    </div>


    <!-- 5. Okul Yönetim Sistemi Görünümü -->


    <!-- Belge Uretici Modali -->
    <div id="document-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.55); z-index:9999; align-items:center; justify-content:center; padding:1rem;">
        <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:1.5rem 0.5rem 1.5rem 1.5rem; width:100%; max-width:540px; box-shadow:0 20px 60px rgba(0,0,0,0.3); box-sizing:border-box; max-height:85vh; display:flex; flex-direction:column;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem; padding-right:1rem;">
                <h3 style="margin:0; color:var(--text-primary); font-size:1.1rem; font-weight:700;">
                    <i data-lucide="printer" size="18" style="vertical-align:middle; margin-right:0.25rem;"></i> Resmi Belge Oluşturucu
                </h3>
                <button onclick="closeDocumentModal()" style="background:none; border:none; cursor:pointer; color:var(--text-secondary); padding:0.25rem;"><i data-lucide="x" size="20"></i></button>
            </div>
            
            <div style="display:flex; flex-direction:column; gap:1rem; overflow-y:auto; flex:1; padding-right:1rem;">
                <!-- Ogrenci Karti Bilgisi -->
                <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:var(--radius-md); padding:0.8rem 1rem; display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.85rem;">
                    <div><span style="color:var(--text-secondary); font-weight:500;">Öğrenci:</span> <strong id="doc-stud-name" style="color:var(--text-primary);"></strong></div>
                    <div><span style="color:var(--text-secondary); font-weight:500;">No:</span> <strong id="doc-stud-no" style="color:var(--text-primary);"></strong></div>
                    <div><span style="color:var(--text-secondary); font-weight:500;">Sınıf/Şube:</span> <strong id="doc-stud-class" style="color:var(--text-primary);"></strong></div>
                    <div><span style="color:var(--text-secondary); font-weight:500;">Tarih:</span> <strong id="doc-current-date" style="color:var(--text-primary);"></strong></div>
                </div>

                <!-- Belge Turu Secimi -->
                <div>
                    <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Belge Türü</label>
                    <select id="doc-type-select" onchange="switchDocumentType()" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                        <option value="izin">İZİN (İzin Tezkeresi)</option>
                        <option value="gec">GEÇ (Geç Kağıdı)</option>
                        <option value="kabul">DERSE KABUL (Derse Kabul Kağıdı)</option>
                        <option value="cagri">ÇAĞRI (Çağrı Pusulası)</option>
                        <option value="veli-izin">VELİ İZİN (Veli İzin Dilekçesi)</option>
                        <option value="uyari">UYARI BELGESİ (Yazılı Uyarı Belgesi)</option>
                    </select>
                </div>

                <!-- Dinamik Form Alanlari -->
                <div id="doc-form-fields" style="display:flex; flex-direction:column; gap:1rem;">
                    <!-- Alanlar JS tarafindan doldurulacak -->
                </div>

                <!-- Onaylayan Seçimi -->
                <div id="doc-approver-section" style="border-top:1px solid var(--border-color); padding-top:1rem; margin-top:0.5rem; display:flex; flex-direction:column; gap:0.5rem;">
                    <label style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); display:flex; align-items:center; gap:0.3rem;">
                        <i data-lucide="user-check" size="14"></i> Onaylayan
                    </label>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div style="position:relative;">
                            <label style="font-size:0.75rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Adı Soyadı</label>
                            <div style="position:relative;">
                                <input type="text" id="doc-approver-name" class="input-field" style="width:100%; box-sizing:border-box; height:40px; padding:0.5rem 2.2rem 0.5rem 0.5rem; font-size:0.85rem;" placeholder="İsim girin veya seçin" autocomplete="off">
                                <button type="button" class="combobox-arrow" style="position:absolute; right:0; top:0; height:100%; width:32px; background:none; border:none; cursor:pointer; color:var(--text-secondary); display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="chevron-down" size="16"></i>
                                </button>
                            </div>
                            <ul id="approver-names-dropdown" style="display:none; position:absolute; left:0; right:0; top:102%; background:var(--bg-card); border:1px solid var(--border-color); border-radius:var(--radius-md); box-shadow:var(--shadow-lg); z-index:10000; list-style:none; padding:0.25rem 0; margin:0;"></ul>
                        </div>
                        <div style="position:relative;">
                            <label style="font-size:0.75rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Ünvanı</label>
                            <div style="position:relative;">
                                <input type="text" id="doc-approver-title" class="input-field" style="width:100%; box-sizing:border-box; height:40px; padding:0.5rem 2.2rem 0.5rem 0.5rem; font-size:0.85rem;" placeholder="Ünvan girin veya seçin" autocomplete="off">
                                <button type="button" class="combobox-arrow" style="position:absolute; right:0; top:0; height:100%; width:32px; background:none; border:none; cursor:pointer; color:var(--text-secondary); display:flex; align-items:center; justify-content:center;">
                                    <i data-lucide="chevron-down" size="16"></i>
                                </button>
                            </div>
                            <ul id="approver-titles-dropdown" style="display:none; position:absolute; left:0; right:0; top:102%; max-height:160px; overflow-y:auto; background:var(--bg-card); border:1px solid var(--border-color); border-radius:var(--radius-md); box-shadow:var(--shadow-lg); z-index:10000; list-style:none; padding:0.25rem 0; margin:0;"></ul>
                        </div>
                    </div>
                </div>

                <!-- Öğrenci Belge Geçmişi (Sicil) -->
                <div id="doc-history-section" style="border-top:1px solid var(--border-color); padding-top:1rem; margin-top:0.5rem; display:flex; flex-direction:column; gap:0.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <label style="font-size:0.8rem; font-weight:700; color:var(--text-secondary); display:flex; align-items:center; gap:0.3rem;">
                            <i data-lucide="history" size="14"></i> Öğrenci İşlem Geçmişi (Son Belgeler)
                        </label>
                        <button id="btn-clear-all-history" onclick="clearAllHistory()" style="display:none; background:none; border:1px solid #fee2e2; border-radius:6px; padding:0.15rem 0.5rem; cursor:pointer; color:#ef4444; font-size:0.72rem; font-weight:600;">Tümünü Temizle</button>
                    </div>
                    <div id="doc-student-history" style="display:flex; flex-direction:column; gap:0.4rem;">
                        <!-- JS tarafından geçmiş listelenecek -->
                    </div>
                </div>
            </div>

            <div style="display:flex; gap:0.75rem; margin-top:1.5rem; justify-content:flex-end; padding-right:1rem;">
                <button onclick="closeDocumentModal()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); border:1px solid var(--border-color); background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-weight:600; font-size:0.875rem;">Kapat</button>
                <button onclick="printDocument()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); background:var(--accent-gradient); color:#fff; border:none; cursor:pointer; font-weight:600; font-size:0.875rem; display:inline-flex; align-items:center; gap:0.4rem;">
                    <i data-lucide="printer" size="16"></i> Belgeyi Yazdır
                </button>
            </div>
        </div>
    </div>

    <!-- Yazdirma Alani (Ekrandayken gizlidir) -->
    <div id="print-section"></div>
    <!-- Karne Baskı Alanı -->
    <div id="karne-print-area" style="display:none;"></div>
    <!-- Supabase Settings Modal -->
    <div id="supabase-settings-modal" class="modal-backdrop" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.55); z-index:9999; align-items:center; justify-content:center; padding:1rem;">
        <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:2rem; width:100%; max-width:480px; box-shadow:0 20px 60px rgba(0,0,0,0.3); border:1px solid var(--border-color); color:var(--text-primary); position:relative;">
            <button onclick="closeSupabaseSettingsModal()" style="position:absolute; right:1.5rem; top:1.5rem; background:none; border:none; color:var(--text-secondary); cursor:pointer; padding:0.25rem;"><i data-lucide="x" size="20"></i></button>
            <h3 style="margin-top:0; margin-bottom:1.25rem; font-size:1.15rem; font-weight:700; display:flex; align-items:center; gap:0.5rem; color:var(--text-primary);"><i data-lucide="database" style="color:var(--accent-color); width:20px; height:20px;"></i> Supabase Ayarları</h3>
            <p style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:1.5rem; line-height:1.5;">
                Verileri bulut üzerinde güvenle saklamak ve diğer cihazlarla senkronize etmek için bağlantı bilgilerini girin. Boş bırakırsanız tarayıcınızın yerel depolama alanını (LocalStorage) kullanmaya devam eder.
            </p>
            <div style="margin-bottom:1.25rem;">
                <label style="display:block; font-size:0.8rem; font-weight:600; margin-bottom:0.4rem;">Supabase Project URL</label>
                <input type="text" id="setting-supabase-url" placeholder="https://xxxx.supabase.co" style="width:100%; height:42px; border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:0 0.75rem; background:var(--bg-page); color:var(--text-primary); box-sizing:border-box; outline:none;">
            </div>
            <div style="margin-bottom:1.5rem;">
                <label style="display:block; font-size:0.8rem; font-weight:600; margin-bottom:0.4rem;">Supabase Anon Key</label>
                <input type="password" id="setting-supabase-key" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." style="width:100%; height:42px; border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:0 0.75rem; background:var(--bg-page); color:var(--text-primary); box-sizing:border-box; outline:none;">
            </div>
            <div style="display:flex; justify-content:flex-end; gap:0.75rem;">
                <button onclick="closeSupabaseSettingsModal()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); border:1px solid var(--border-color); background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-weight:600; font-size:0.875rem;">Kapat</button>
                <button onclick="saveSupabaseSettings()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); background:var(--accent-gradient); color:#fff; border:none; cursor:pointer; font-weight:600; font-size:0.875rem; display:inline-flex; align-items:center; gap:0.4rem; box-shadow:var(--shadow-sm);"><i data-lucide="check" size="16"></i> Kaydet ve Bağlan</button>
            </div>
        </div>
    </div>

    <!-- Okul Yönetim Kayıt Modal -->
    <div id="school-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.55); z-index:9999; align-items:center; justify-content:center; padding:1rem;">
        <div style="background:var(--bg-card); border-radius:var(--radius-lg); padding:1.5rem 0.5rem 1.5rem 1.5rem; width:100%; max-width:480px; box-shadow:0 20px 60px rgba(0,0,0,0.3); max-height:85vh; display:flex; flex-direction:column;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem; padding-right:1rem;">
                <h3 id="school-modal-title" style="margin:0; color:var(--text-primary); font-size:1.1rem;">Yeni Kayıt Ekle</h3>
                <button onclick="closeSchoolModal()" style="background:none; border:none; cursor:pointer; color:var(--text-secondary); padding:0.25rem;"><i data-lucide="x" size="20"></i></button>
            </div>
            <div id="school-modal-body" style="display:flex; flex-direction:column; gap:1rem; overflow-y:auto; flex:1; padding-right:1rem;"></div>
            <div style="display:flex; gap:0.75rem; margin-top:1.5rem; justify-content:flex-end; padding-right:1rem;">
                <button onclick="closeSchoolModal()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); border:1px solid var(--border-color); background:var(--bg-card); color:var(--text-primary); cursor:pointer; font-weight:600; font-size:0.875rem;">İptal</button>
                <button onclick="saveSchoolRecord()" style="padding:0.6rem 1.25rem; border-radius:var(--radius-lg); background:var(--accent-gradient); color:#fff; border:none; cursor:pointer; font-weight:600; font-size:0.875rem;">Kaydet</button>
            </div>
        </div>
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
                <label for="password-input" style="color:#64748b;">Giriş Şifresi</label>
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

    <!-- MOBILE BOTTOM NAVIGATION BAR (Only for Analysis View) -->
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

    <!-- Redesigned Footer (Modern Layout) -->
    <footer>
        <div class="footer-content">
            <div class="footer-col">
                <h4><i data-lucide="map-pin"></i> Adres</h4>
                <p>Yenişehir Mah. Seyfullah Hacımütfüoğlu Cad. No: 5<br>Ceylanpınar / Şanlıurfa</p>
            </div>
            <div class="footer-col">
                <h4><i data-lucide="phone"></i> Telefon</h4>
                <p><a href="tel:04144713519" style="color: inherit; text-decoration: none;">0414 471 35 19</a></p>
            </div>
            <div class="footer-col">
                <h4><i data-lucide="instagram"></i> Instagram</h4>
                <p><a href="https://www.instagram.com/cfenlisesi/" target="_blank" style="color: #3b82f6 !important; text-decoration: underline !important; font-weight: 600;">@cfenlisesi</a></p>
            </div>
        </div>
    </footer>

    <script>
        // Global Hata Yakalayıcı (Arayüzde kırmızı kutuda hata gösterimi için)
        window.addEventListener('error', function(e) {
            const errDiv = document.createElement('div');
            errDiv.style.cssText = 'position:fixed; bottom:15px; left:15px; background:rgba(220,38,38,0.96); color:white; padding:12px; border-radius:10px; font-family:monospace; font-size:11px; z-index:999999; max-width:85%; box-shadow:0 10px 25px rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); line-height:1.4;';
            errDiv.innerHTML = '<strong style="font-size:12px; display:block; margin-bottom:4px;">❌ Tarayıcı Hatası Yakalandı</strong>' + e.message + '<br><small style="color:rgba(255,255,255,0.7); display:block; margin-top:4px;">Dosya: ' + (e.filename || '').split('/').pop() + ':' + e.lineno + '</small>';
            document.body.appendChild(errDiv);
        });

        window.addEventListener('unhandledrejection', function(e) {
            const errDiv = document.createElement('div');
            errDiv.style.cssText = 'position:fixed; bottom:15px; left:15px; background:rgba(220,38,38,0.96); color:white; padding:12px; border-radius:10px; font-family:monospace; font-size:11px; z-index:999999; max-width:85%; box-shadow:0 10px 25px rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); line-height:1.4;';
            errDiv.innerHTML = '<strong style="font-size:12px; display:block; margin-bottom:4px;">⚠️ Promise Hatası Yakalandı</strong>' + e.reason;
            document.body.appendChild(errDiv);
        });

        // Default dataset embedded from Python extraction
        const DEFAULT_DATA = /* DATABASE_PLACEHOLDER */;
        const DEFAULT_OKUL_DB = /* OKUL_DATABASE_PLACEHOLDER */;

        let db = null;
        let schoolData = null;
        let currentSchoolTab = 'ogrenci';
        let schoolEditId = null;
        let selectedDocStudent = null;
        let examDatabase = [];
        let activeStudent = null;
        let progressChart = null;
        let isNavigating = false; // History Router flag

        // Supabase Client Global Config
        let supabaseClient = null;
        let supabaseUrl = 'https://vpzreuhkgyekiavrrlcc.supabase.co';
        let supabaseKey = 'sb_publishable_ZXcSkt85QMD0Ply08h0B1A_0cEAUhdu';

        // Initialize App
        window.addEventListener('DOMContentLoaded', () => {
            // CDN kütüphanelerinin (Lucide, ChartJS vb.) yüklenememe durumuna karşı korumalı (try/catch) başlatma
            try {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                } else {
                    console.error("Lucide CDN could not be loaded.");
                }
            } catch (e) {
                console.error("Lucide init error:", e);
            }

            try { initTheme(); } catch (e) { console.error("Theme init error:", e); }
            try { initSearch(); } catch (e) { console.error("Search init error:", e); }
            try { setupDragAndDrop(); } catch (e) { console.error("DragAndDrop init error:", e); }
            try { initNewsFetcher(); } catch (e) { console.error("NewsFetcher init error:", e); }
            try { initSupabase(); } catch (e) { console.error("Supabase init error:", e); }
            try { 
                loadSchoolData().then(() => {
                    loadExamData();
                });
            } catch (e) { console.error("Data load init error:", e); }
            try { initRouter(); } catch (e) { console.error("Router init error:", e); }
            
            // ESC tuşu ile modalları kapatma desteği
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Escape') {
                    const docModal = document.getElementById('document-modal');
                    const schoolModal = document.getElementById('school-modal');
                    const loginModal = document.getElementById('login-modal');
                    
                    if (docModal && docModal.style.display !== 'none') {
                        closeDocumentModal();
                    }
                    if (schoolModal && schoolModal.style.display !== 'none') {
                        closeSchoolModal();
                    }
                    if (loginModal && loginModal.classList.contains('open')) {
                        closeLoginModal();
                    }
                    const settingsModal = document.getElementById('supabase-settings-modal');
                    if (settingsModal && settingsModal.style.display !== 'none') {
                        closeSupabaseSettingsModal();
                    }
                }
            });
        });

        // Theme management
        function initSupabase() {
            const savedUrl = localStorage.getItem('supabase_url') || supabaseUrl;
            const savedKey = localStorage.getItem('supabase_key') || supabaseKey;

            if (savedUrl && savedUrl !== 'YOUR_SUPABASE_URL' && savedKey && savedKey !== 'YOUR_SUPABASE_ANON_KEY') {
                try {
                    // supabase global scriptinden istemciyi oluşturuyoruz
                    if (typeof supabasejs !== 'undefined') {
                        supabaseClient = supabase.createClient(savedUrl, savedKey);
                        console.log("Supabase connection successfully established!");
                    } else if (typeof window.supabase !== 'undefined') {
                        supabaseClient = window.supabase.createClient(savedUrl, savedKey);
                        console.log("Supabase connection successfully established via window!");
                    }
                } catch(e) {
                    console.error("Supabase client creation failed:", e);
                }
            } else {
                console.log("Supabase not configured. Using browser local storage mode.");
            }
        }

        function openSupabaseSettingsModal() {
            document.getElementById('setting-supabase-url').value = localStorage.getItem('supabase_url') || (supabaseUrl !== 'YOUR_SUPABASE_URL' ? supabaseUrl : '');
            document.getElementById('setting-supabase-key').value = localStorage.getItem('supabase_key') || (supabaseKey !== 'YOUR_SUPABASE_ANON_KEY' ? supabaseKey : '');
            document.getElementById('supabase-settings-modal').style.display = 'flex';
        }

        function closeSupabaseSettingsModal() {
            document.getElementById('supabase-settings-modal').style.display = 'none';
        }

        function saveSupabaseSettings() {
            let url = document.getElementById('setting-supabase-url').value.trim();
            const key = document.getElementById('setting-supabase-key').value.trim();
            
            if (url) {
                // Eğer sadece Project ID girildiyse (örn: vpzreuhkgyekiavrrIcc) bunu tam URL'e dönüştür
                if (!url.startsWith('http://') && !url.startsWith('https://')) {
                    url = `https://${url}.supabase.co`;
                }
                localStorage.setItem('supabase_url', url);
            } else {
                localStorage.removeItem('supabase_url');
            }

            if (key) {
                localStorage.setItem('supabase_key', key);
            } else {
                localStorage.removeItem('supabase_key');
            }

            showToast("Bağlantı bilgileri kaydedildi! Portal yeniden başlatılıyor...");
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }

        function updateDbStatusBadge(isCloud) {
            const badge = document.getElementById('db-status-badge');
            const dot = document.getElementById('db-status-dot');
            if (!badge || !dot) return;

            if (isCloud) {
                badge.style.background = 'rgba(16,185,129,0.08)';
                badge.style.borderColor = 'rgba(16,185,129,0.2)';
                badge.title = 'Bulut Bağlantısı Aktif (Supabase)';
                dot.style.background = '#10b981';
                dot.style.boxShadow = '0 0 6px #10b981';
            } else {
                badge.style.background = 'rgba(239,68,68,0.08)';
                badge.style.borderColor = 'rgba(239,68,68,0.2)';
                badge.title = 'Bağlantı Yok (Çevrimdışı)';
                dot.style.background = '#ef4444';
                dot.style.boxShadow = '0 0 6px #ef4444';
            }
        }

        function initTheme() {
            const currentTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', currentTheme);
            updateThemeButtonIcon(currentTheme);
        }

        function toggleTheme() {
            // Tema geçişinde binlerce elemanın transition yükünü kaldırmak için geçici olarak animasyonları kapatıyoruz
            document.documentElement.classList.add('disable-transitions');

            const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateThemeButtonIcon(theme);
            if (activeStudent) {
                renderProgressChart(activeStudent); // redraw chart with new colors
            }

            // Render işlemi tamamlandıktan hemen sonra geçişleri geri açıyoruz (anlık geçiş sağlanmış olur)
            setTimeout(() => {
                document.documentElement.classList.remove('disable-transitions');
            }, 30);
        }

        function updateThemeButtonIcon(theme) {
            const btn = document.getElementById('theme-btn');
            if (!btn) return;
            if (theme === 'dark') {
                btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>';
            } else {
                btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>';
            }
        }

        // e-Okul News Scraper/Proxy Parser (Uses JSON endpoint for stability)
        function initNewsFetcher() {
            const targetUrl = 'https://ceylanpinarfenlisesi.meb.k12.tr';
            const proxyUrl = 'https://api.allorigins.win/get?url=' + encodeURIComponent(targetUrl);

            fetch(proxyUrl)
                .then(response => {
                    if (response.ok) return response.json();
                    throw new Error('CORS proxy response was not ok.');
                })
                .then(data => {
                    const htmlContent = data.contents;
                    if (!htmlContent) throw new Error('Proxy returned empty content.');
                    
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(htmlContent, 'text/html');

                    // Parse news items
                    const news = [];
                    const newsAnchors = doc.querySelectorAll('#haber_blok a');
                    newsAnchors.forEach(a => {
                        const href = a.getAttribute('href');
                        const title = a.textContent.trim();
                        if (href && href.startsWith('/icerikler/') && !title.toLowerCase().includes('devamı')) {
                            news.push({
                                title: title,
                                url: targetUrl + href
                            });
                        }
                    });

                    // Parse announcement items
                    const announcements = [];
                    const duyuruAnchors = doc.querySelectorAll('#duyuru_blok a');
                    duyuruAnchors.forEach(a => {
                        const href = a.getAttribute('href');
                        const title = a.textContent.trim();
                        if (href && href.startsWith('/icerikler/') && !title.toLowerCase().includes('devamı')) {
                            announcements.push({
                                title: title,
                                url: targetUrl + href
                            });
                        }
                    });

                    // Parse slider featured items
                    const slider = [];
                    const sliderAnchors = doc.querySelectorAll('#slider a');
                    sliderAnchors.forEach(a => {
                        const href = a.getAttribute('href');
                        const span = a.querySelector('span');
                        const title = span ? span.textContent.trim() : a.textContent.trim();
                        if (href && href.startsWith('/icerikler/')) {
                            slider.push({
                                title: title,
                                url: targetUrl + href
                            });
                        }
                    });

                    updateNewsColumns(news, announcements, slider);
                })
                .catch(err => {
                    console.warn("Could not fetch live MEB news at runtime:", err);
                });
        }

        function updateNewsColumns(news, announcements, slider) {
            const leftColContainer = document.getElementById('left-news-list');
            const rightColContainer = document.getElementById('right-news-list');

            // Left Column items (Haberler)
            let leftItems = [];
            if (news.length > 0) {
                leftItems = news.slice(0, 3);
            } else if (slider.length > 0) {
                leftItems = slider.slice(0, 2);
            }

            // Right Column items (Duyurular)
            let rightItems = [];
            if (announcements.length > 0) {
                rightItems = announcements.slice(0, 3);
            } else {
                const remainingNews = news.slice(3);
                if (remainingNews.length > 0) {
                    rightItems = remainingNews.slice(0, 2);
                } else {
                    const remainingSlider = slider.filter(s => !leftItems.some(l => l.url === s.url));
                    if (remainingSlider.length > 0) {
                        rightItems = remainingSlider.slice(0, 2);
                    }
                }
            }

            // Render Left Column
            if (leftItems.length > 0) {
                leftColContainer.innerHTML = '<h3><i data-lucide="megaphone" size="20"></i> Haberler ve Duyurular</h3>' + 
                    leftItems.map((item, idx) => `
                        <a href="${item.url}" target="_blank" class="news-card">
                            ${idx === 0 ? '<span class="ribbon">Yeni</span>' : ''}
                            <div class="news-icon-wrapper">
                                <i data-lucide="${idx === 0 ? 'bell' : 'calendar'}" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>${item.title}</h4>
                                <p>Ceylanpınar Fen Lisesi resmi haber duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                    `).join('');
            }

            // Render Right Column
            if (rightItems.length > 0) {
                rightColContainer.innerHTML = '<h3><i data-lucide="award" size="20"></i> Sınav ve Gelişim Duyuruları</h3>' + 
                    rightItems.map((item, idx) => `
                        <a href="${item.url}" target="_blank" class="news-card">
                            <div class="news-icon-wrapper">
                                <i data-lucide="file-text" size="20"></i>
                            </div>
                            <div class="news-content">
                                <h4>${item.title}</h4>
                                <p>Ceylanpınar Fen Lisesi resmi sınav ve gelişim duyurusu.</p>
                            </div>
                            <i data-lucide="chevron-right" class="news-arrow" size="16"></i>
                        </a>
                    `).join('');
            }

            lucide.createIcons();
        }

        // Browser Navigation (HTML5 History API Router - Protected)
        function initRouter() {
            let currentHash = window.location.hash || '#home';
            let stateName = currentHash.replace('#', '');
            
            window.history.replaceState({ state: stateName }, "", currentHash);
            navigate(stateName, false);

            window.addEventListener('popstate', (event) => {
                let targetState = 'home';
                if (event.state && event.state.state) {
                    targetState = event.state.state;
                } else if (window.location.hash) {
                    targetState = window.location.hash.replace('#', '');
                }
                navigate(targetState, false);
            });
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
                // On desktop, show karne & graphic, hide mobile-only tabs
                document.getElementById('analysis-tab-karne').style.display = 'flex';
                document.getElementById('analysis-tab-grafik').style.display = 'block';
                document.getElementById('analysis-tab-istatistik').style.display = 'none';
                document.getElementById('analysis-tab-ayarlar').style.display = 'none';
            } else {
                // If resized back to mobile, maintain active tabs
                if (document.getElementById('teacher-analysis-view').style.display !== 'none') {
                    const activeAnalysisTab = document.querySelector('#mobile-nav-analysis .mobile-nav-item.active').id.replace('nav-analysis-', '');
                    switchAnalysisTab(activeAnalysisTab);
                }
            }
        });

        // Supabase Exam Data Loading
        async function loadExamData() {
            if (supabaseClient) {
                try {
                    const { data, error } = await supabaseClient
                        .from('exam_results')
                        .select('*')
                        .order('id', { ascending: true });
                    
                    if (error) {
                        console.error("Supabase loadExamData query error:", error);
                        examDatabase = [];
                    } else {
                        examDatabase = (data || []).map(r => ({
                            id: r.id,
                            no: r.student_no,
                            name: r.student_name,
                            class: r.student_class,
                            branch: r.student_branch,
                            subjects: r.subjects,
                            puan: r.puan,
                            siralama: r.siralama,
                            deneme: r.exam_name
                        }));
                        console.log(`Loaded ${examDatabase.length} records from Supabase!`);
                    }
                } catch (e) {
                    console.error("Supabase loadExamData exception:", e);
                    examDatabase = [];
                }
            } else {
                examDatabase = [];
            }
            refreshDashboard();
        }

                function applyRolePermissions() {
            const role = sessionStorage.getItem('user_role') || 'student';
            
            const desktopUpload = document.getElementById('sidebar-upload-card');
            const desktopReset = document.getElementById('sidebar-reset-card');
            const mobileUpload = document.getElementById('mobile-upload-section');
            const mobileReset = document.getElementById('mobile-reset-section');
            const schoolAddBtn = document.getElementById('school-add-btn');
            
            if (role === 'admin') {
                if (desktopUpload) desktopUpload.style.display = 'block';
                if (desktopReset) desktopReset.style.display = 'block';
                if (mobileUpload) mobileUpload.style.display = 'flex';
                if (mobileReset) mobileReset.style.display = 'flex';
                if (schoolAddBtn) schoolAddBtn.style.display = 'inline-flex';
            } else {
                // Öğretmen veya diğer durumlar için
                if (desktopUpload) desktopUpload.style.display = 'none';
                if (desktopReset) desktopReset.style.display = 'none';
                if (mobileUpload) mobileUpload.style.display = 'none';
                if (mobileReset) mobileReset.style.display = 'none';
                if (schoolAddBtn) schoolAddBtn.style.display = 'none';
            }
        }

function navigate(state, push = true) {
            if (isNavigating) return;
            isNavigating = true;

            try {
                let loggedIn = false;
                try {
                    loggedIn = sessionStorage.getItem('teacher_logged_in') === 'true';
                } catch(e) {}

                // Authorization guards
                if ((state === 'teacher-hub' || state === 'teacher-analysis' || state === 'school-management') && !loggedIn) {
                    state = 'home';
                    push = false;
                    window.history.replaceState({ state: 'home' }, "", '#home');
                }

                // Execute switches
                if (state === 'home') {
                    showSelectionScreenView();
                } else if (state === 'student-hub') {
                    showStudentHubView();
                } else if (state === 'teacher-hub') {
                    showTeacherHubView();
                } else if (state === 'teacher-analysis') {
                    showTeacherAnalysisViewView();
                } else if (state === 'school-management') {
                    showSchoolManagementView();
                }

                applyRolePermissions();

                if (push) {
                    window.history.pushState({ state: state }, "", '#' + state);
                }
            } catch (err) {
                console.error("Router navigation exception:", err);
            } finally {
                isNavigating = false;
            }
        }

        function goBack(fallback) {
            if (window.history.length > 1) {
                window.history.back();
            } else {
                navigate(fallback);
            }
        }

        function handleLogoClick() {
            navigate('home');
        }

        // Password modal handlers
                function clearSearchInput(inputId) {
            const input = document.getElementById(inputId);
            if (!input) return;
            input.value = '';
            
            const btnId = inputId === 'search-student' ? 'clear-search-student' : 'clear-school-search';
            const btn = document.getElementById(btnId);
            if (btn) btn.style.display = 'none';

            if (inputId === 'search-student') {
                document.getElementById('search-results-list').style.display = 'none';
            } else if (inputId === 'school-search-input') {
                renderSchoolTable();
            }
            input.focus();
        }

        function handleSchoolSearchInput() {
            const input = document.getElementById('school-search-input');
            const clearBtn = document.getElementById('clear-school-search');
            if (clearBtn && input) {
                clearBtn.style.display = input.value.trim().length > 0 ? 'inline-flex' : 'none';
            }
            renderSchoolTable();
        }

function verifyPassword() {
            const passwordVal = document.getElementById('password-input').value.trim();
            if (passwordVal === 'müdür2014') {
                try {
                    sessionStorage.setItem('teacher_logged_in', 'true');
                    sessionStorage.setItem('user_role', 'admin');
                } catch (e) {}
                closeLoginModal();
                navigate('teacher-hub');
            } else if (passwordVal === 'ceylanpinar2014') {
                try {
                    sessionStorage.setItem('teacher_logged_in', 'true');
                    sessionStorage.setItem('user_role', 'teacher');
                } catch (e) {}
                closeLoginModal();
                navigate('teacher-hub');
            } else {
                document.getElementById('login-error').style.display = 'block';
                document.getElementById('password-input').value = '';
                document.getElementById('password-input').focus();
            }
        }

        function logout() {
            try {
                sessionStorage.removeItem('teacher_logged_in');
                sessionStorage.removeItem('user_role');
            } catch (e) {}
            navigate('home');
        }

        function openLoginModal() {
            document.getElementById('login-modal').classList.add('open');
            document.getElementById('password-input').focus();
            document.getElementById('login-error').style.display = 'none';
        }

        function closeLoginModal() {
            document.getElementById('login-modal').classList.remove('open');
            document.getElementById('password-input').value = '';
        }

        function handlePasswordKeydown(event) {
            if (event.key === 'Enter') {
                verifyPassword();
            }
        }

        // View Renderers
        function showSelectionScreenView() {
            document.body.classList.add('portal-mode');
            document.getElementById('app-container').classList.add('no-sidebar');
            
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('school-management-view').style.display = 'none';
            document.getElementById('selection-screen').style.display = 'flex';
            
            document.getElementById('logout-btn').style.display = 'none';
            document.getElementById('header-logo-section').style.display = 'none'; // Hidden on home selection screen
            
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
        }

        function showStudentHubView() {
            document.body.classList.add('portal-mode');
            document.getElementById('app-container').classList.add('no-sidebar');
            
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('school-management-view').style.display = 'none';
            document.getElementById('student-hub').style.display = 'block';
            
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-logo-section').style.display = 'flex'; // Visible
            document.getElementById('header-title').innerText = 'Ceylanpınar Fen Lisesi';
            document.getElementById('header-subtitle').innerText = 'Öğrenci Portalı';
            
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
        }

        function showTeacherHubView() {
            document.body.classList.add('portal-mode');
            document.getElementById('app-container').classList.add('no-sidebar');
            
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('school-management-view').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'block';
            
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-logo-section').style.display = 'flex'; // Visible
            document.getElementById('header-title').innerText = 'Ceylanpınar Fen Lisesi';
            document.getElementById('header-subtitle').innerText = 'Öğretmen Portalı';
            
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');
        }

        function showTeacherAnalysisViewView() {
            document.body.classList.remove('portal-mode');
            document.getElementById('app-container').classList.remove('no-sidebar');
            
            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('school-management-view').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'flex';
            
            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-logo-section').style.display = 'flex'; // Visible
            document.getElementById('header-title').innerText = 'Ceylanpınar Fen Lisesi';
            document.getElementById('header-subtitle').innerText = 'Öğretmen Portalı';
            
            document.getElementById('mobile-nav-analysis').style.display = ''; // let CSS override (flex in mobile)
            
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                switchAnalysisTab('karne');
            } else {
                document.getElementById('analysis-tab-karne').style.display = 'flex';
                document.getElementById('analysis-tab-grafik').style.display = 'block';
                document.getElementById('analysis-tab-istatistik').style.display = 'none';
                document.getElementById('analysis-tab-ayarlar').style.display = 'none';
            }
            
            refreshDashboard();
        }



        // Belge Uretici Fonksiyonlari
                        // Custom Autocomplete Combobox Lojiği
        window.selectOption = function(inputId, dropdownId, val) {
            const input = document.getElementById(inputId);
            const dropdown = document.getElementById(dropdownId);
            if (input) {
                input.value = val;
                input.dispatchEvent(new Event('input'));
            }
            if (dropdown) dropdown.style.display = 'none';
        };

        function initCustomCombobox(inputId, dropdownId, getOptionsFn) {
            const input = document.getElementById(inputId);
            const dropdown = document.getElementById(dropdownId);
            if (!input || !dropdown) return;
            
            const container = input.parentElement; // gets parent relative div containing input and arrow
            const arrowBtn = container.querySelector('.combobox-arrow');
            if (!arrowBtn) return;
            
            function renderList(filterText = '') {
                const options = getOptionsFn() || [];
                const filtered = options.filter(opt => 
                    opt.toLowerCase().includes(filterText.toLowerCase())
                );
                
                if (filtered.length === 0) {
                    dropdown.style.display = 'none';
                    return;
                }
                
                dropdown.innerHTML = filtered.map(opt => {
                    const escapedOpt = opt.replace(/'/g, "\'");
                    return `
                        <li class="combobox-item" style="padding:0.5rem 0.75rem; cursor:pointer; font-size:0.825rem; color:var(--text-primary); transition:background 0.15s;" 
                            onmouseover="this.style.background='var(--bg-page)'" 
                            onmouseout="this.style.background='none'"
                            onclick="selectOption('${inputId}', '${dropdownId}', '${escapedOpt}')">
                            ${opt}
                        </li>
                    `;
                }).join('');
                dropdown.style.display = 'block';
            }
            
            function showAll() {
                const isVisible = dropdown.style.display === 'block';
                if (isVisible) {
                    dropdown.style.display = 'none';
                } else {
                    renderList(''); // Boş filtre ile tümünü getir
                }
            }
            
            if (!input.dataset.comboboxBound) {
                input.addEventListener('input', function() {
                    renderList(this.value);
                });
                
                arrowBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    showAll();
                });
                
                // Dışarı tıklanınca kapat
                document.addEventListener('click', function(e) {
                    if (!container.parentElement.contains(e.target)) {
                        dropdown.style.display = 'none';
                    }
                });
                
                input.dataset.comboboxBound = "true";
            }
        }

function renderStudentHistory(student) {
            const container = document.getElementById('doc-student-history');
            if (!container) return;
            
            const clearAllBtn = document.getElementById('btn-clear-all-history');
            
            if (!student.history || student.history.length === 0) {
                container.innerHTML = `
                    <div style="background:rgba(16,185,129,0.06); border:1px dashed rgba(16,185,129,0.25); border-radius:8px; padding:0.6rem; text-align:center; color:#10b981; font-size:0.78rem; font-weight:500;">
                        <i data-lucide="check-circle" size="14" style="vertical-align:middle; margin-right:0.2rem;"></i> Bu öğrenciye ait geçmiş belge bulunmamaktadır (Temiz Sicil)
                    </div>
                `;
                if (clearAllBtn) clearAllBtn.style.display = 'none';
            } else {
                let html = '';
                student.history.forEach((item, idx) => {
                    const deleteBtn = (sessionStorage.getItem('user_role') === 'admin')
                        ? `<button onclick="deleteHistoryItem(${idx})" style="background:none; border:none; cursor:pointer; color:#ef4444; padding:0 0.2rem; font-size:0.78rem; line-height:1;" title="Bu kaydı sil">✕</button>`
                        : '';
                    html += `
                        <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:6px; padding:0.5rem 0.75rem; font-size:0.76rem; display:flex; flex-direction:column; gap:0.15rem; text-align:left;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <strong style="color:var(--text-primary);">${item.tur}</strong>
                                <div style="display:flex; align-items:center; gap:0.4rem;">
                                    <span style="color:var(--text-secondary); font-size:0.7rem; font-weight:500;">${item.tarih}</span>
                                    ${deleteBtn}
                                </div>
                            </div>
                            <span style="color:var(--text-secondary); line-height:1.2;">${item.detay}</span>
                        </div>
                    `;
                });
                container.innerHTML = html;
                if (clearAllBtn) clearAllBtn.style.display = (sessionStorage.getItem('user_role') === 'admin') ? 'inline-block' : 'none';
            }
            if (window.lucide) lucide.createIcons();
        }
        
        async function deleteHistoryItem(index) {
            if (!selectedDocStudent || !selectedDocStudent.history) return;
            if (!confirm('Bu geçmiş kaydı silinsin mi?')) return;
            
            const item = selectedDocStudent.history[index];
            if (supabaseClient && item.id) {
                const { error } = await supabaseClient.from('document_history').delete().eq('id', item.id);
                if (error) { alert('Silme hatası: ' + error.message); return; }
            }
            
            selectedDocStudent.history.splice(index, 1);
            persistSchoolData();
            renderStudentHistory(selectedDocStudent);
        }
        
        async function clearAllHistory() {
            if (!selectedDocStudent) return;
            if (!confirm('Bu öğrenciye ait tüm geçmiş kayıtlar silinsin mi?')) return;
            
            if (supabaseClient) {
                const { error } = await supabaseClient.from('document_history').delete().eq('student_no', selectedDocStudent.no);
                if (error) { alert('Temizleme hatası: ' + error.message); return; }
            }
            
            selectedDocStudent.history = [];
            persistSchoolData();
            renderStudentHistory(selectedDocStudent);
        }

function openDocumentModal(studentNo) {
            let student = null;
            if (String(studentNo) === 'ADI') {
                student = {
                    no: 'ADI',
                    ad: 'İsimsiz',
                    soyad: 'Belge',
                    snf: '',
                    sube: ''
                };
            } else {
                student = schoolData.ogrenci.find(s => String(s.no) === String(studentNo));
            }
            if (!student) return;
            selectedDocStudent = student;
            
            const isAnonymous = String(student.no) === 'ADI';
            if (isAnonymous) {
                document.getElementById('doc-stud-name').innerText = "Boş Şablon (İsimsiz)";
                document.getElementById('doc-stud-no').innerText = "........................";
                document.getElementById('doc-stud-class').innerText = "........................";
            } else {
                document.getElementById('doc-stud-name').innerText = (student.ad || '') + ' ' + (student.soyad || '');
                document.getElementById('doc-stud-no').innerText = student.no || '-';
                
                const displayClass = student.snf ? (student.snf + (student.sube ? '/' + student.sube : '')) : '-';
                document.getElementById('doc-stud-class').innerText = displayClass;
            }

            const today = new Date();
            const dateStr = today.getDate().toString().padStart(2, '0') + '/' + 
                            (today.getMonth() + 1).toString().padStart(2, '0') + '/' + 
                            today.getFullYear();
            document.getElementById('doc-current-date').innerText = dateStr;

            document.getElementById('doc-type-select').value = 'izin';
            switchDocumentType();
            
            // Öğrenci Geçmişi Görünürlük Kontrolü
            const historySection = document.getElementById('doc-history-section');
            if (historySection) {
                if (isAnonymous) {
                    historySection.style.setProperty('display', 'none', 'important');
                } else {
                    historySection.style.setProperty('display', 'flex', 'important');
                }
            }
            
            renderStudentHistory(student);
            
            // Onaylayan custom combobox'larını ilklendir ve varsayılan idareciyi ata
            if (schoolData && schoolData.idare) {
                const getNames = () => [...new Set(schoolData.idare.map(adm => adm.ad_soyad).filter(Boolean))];
                const getTitles = () => [...new Set(schoolData.idare.map(adm => adm.unvan).filter(Boolean))];
                
                initCustomCombobox('doc-approver-name', 'approver-names-dropdown', getNames);
                initCustomCombobox('doc-approver-title', 'approver-titles-dropdown', getTitles);
                
                const defaultAdmin = schoolData.idare[0];
                if (defaultAdmin) {
                    document.getElementById('doc-approver-name').value = defaultAdmin.ad_soyad || '';
                    document.getElementById('doc-approver-title').value = defaultAdmin.unvan || '';
                } else {
                    document.getElementById('doc-approver-name').value = '';
                    document.getElementById('doc-approver-title').value = '';
                }
            }

            document.getElementById('document-modal').style.display = 'flex';
            if (window.lucide) lucide.createIcons();
        }

        function closeDocumentModal() {
            document.getElementById('document-modal').style.display = 'none';
            selectedDocStudent = null;
        }

                function switchDocumentType() {
            const docType = document.getElementById('doc-type-select').value;
            const container = document.getElementById('doc-form-fields');
            let fields = '';
            
            const today = new Date().toISOString().substring(0, 10);

            // Dinamik ogretmen ve idare seceneklerini hazirla
            let ogretmenOptions = '<option value="">Öğretmen Seçin...</option>';
            if (schoolData && schoolData.ogretmen) {
                schoolData.ogretmen.forEach(o => {
                    if (o.ad_soyad !== "Ders Öğretmeni") {
                        ogretmenOptions += `<option value="${o.ad_soyad}">${o.ad_soyad}</option>`;
                    }
                });
            }

            let idareOptions = '<option value="">İdareci Seçin...</option>';
            if (schoolData && schoolData.idare) {
                schoolData.idare.forEach(i => {
                    idareOptions += `<option value="${i.ad_soyad}">${i.ad_soyad} (${i.unvan})</option>`;
                });
            }

            if (docType === 'izin') {
                fields = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">İzin Başlangıç Saati</label>
                            <select id="df-izin-baslangic-saat" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="1.DERS SAATİ">1.DERS SAATİ</option>
                                <option value="2.DERS SAATİ">2.DERS SAATİ</option>
                                <option value="3.DERS SAATİ">3.DERS SAATİ</option>
                                <option value="4.DERS SAATİ">4.DERS SAATİ</option>
                                <option value="5.DERS SAATİ">5.DERS SAATİ</option>
                                <option value="6.DERS SAATİ">6.DERS SAATİ</option>
                                <option value="7.DERS SAATİ">7.DERS SAATİ</option>
                                <option value="8.DERS SAATİ">8.DERS SAATİ</option>
                                <option value="TAM GÜN">TAM GÜN</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">İzin Bitiş Saati</label>
                            <select id="df-izin-bitis-saat" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="DERS SAATİ">DERS SAATİ</option>
                                <option value="1.DERS SAATİ">1.DERS SAATİ</option>
                                <option value="2.DERS SAATİ">2.DERS SAATİ</option>
                                <option value="3.DERS SAATİ">3.DERS SAATİ</option>
                                <option value="4.DERS SAATİ">4.DERS SAATİ</option>
                                <option value="5.DERS SAATİ">5.DERS SAATİ</option>
                                <option value="6.DERS SAATİ">6.DERS SAATİ</option>
                                <option value="7.DERS SAATİ">7.DERS SAATİ</option>
                                <option value="8.DERS SAATİ">8.DERS SAATİ</option>
                                <option value="TAM GÜN">TAM GÜN</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">İzin Mazereti</label>
                        <select id="df-izin-neden" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                            <option value="Hastalık izni">Hastalık izni</option>
                            <option value="Ailesinin Taziyesi">Ailesinin Taziyesi</option>
                            <option value="Ailesinin Düğünü">Ailesinin Düğünü</option>
                            <option value="Ailesinin Şehir dışına çıkması">Ailesinin Şehir dışına çıkması</option>
                            <option value="Ailenin isteği">Ailenin isteği</option>
                            <option value="İdarenin izni">İdarenin izni</option>
                            <option value="Diğer İzinler">Diğer İzinler</option>
                        </select>
                    </div>
                `;
            } else if (docType === 'gec') {
                fields = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Saati</label>
                            <select id="df-gec-ders-saat" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="1.DERS SAATİ">1.DERS SAATİ</option>
                                <option value="2.DERS SAATİ">2.DERS SAATİ</option>
                                <option value="3.DERS SAATİ">3.DERS SAATİ</option>
                                <option value="4.DERS SAATİ">4.DERS SAATİ</option>
                                <option value="5.DERS SAATİ">5.DERS SAATİ</option>
                                <option value="6.DERS SAATİ">6.DERS SAATİ</option>
                                <option value="7.DERS SAATİ">7.DERS SAATİ</option>
                                <option value="8.DERS SAATİ">8.DERS SAATİ</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Geç Mazereti</label>
                            <select id="df-gec-neden" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="Servis Aracının Gecikmesi">Servis Aracının Gecikmesi</option>
                                <option value="Öğrencinin Uykuda Kalması">Öğrencinin Uykuda Kalması</option>
                                <option value="Ulaşım Aracının Gecikmesi">Ulaşım Aracının Gecikmesi</option>
                                <option value="Öğrencinin Yurt Nöbeti">Öğrencinin Yurt Nöbeti</option>
                                <option value="İklim Şartları">İklim Şartları</option>
                                <option value="Diğer Sebepler">Diğer Sebepler</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Öğretmeni</label>
                        <select id="df-gec-ogretmen" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                            ${ogretmenOptions}
                        </select>
                    </div>
                `;
            } else if (docType === 'kabul') {
                fields = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Saati</label>
                            <select id="df-kabul-saat" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="1.DERS SAATİ">1.DERS SAATİ</option>
                                <option value="2.DERS SAATİ">2.DERS SAATİ</option>
                                <option value="3.DERS SAATİ">3.DERS SAATİ</option>
                                <option value="4.DERS SAATİ">4.DERS SAATİ</option>
                                <option value="5.DERS SAATİ">5.DERS SAATİ</option>
                                <option value="6.DERS SAATİ">6.DERS SAATİ</option>
                                <option value="7.DERS SAATİ">7.DERS SAATİ</option>
                                <option value="8.DERS SAATİ">8.DERS SAATİ</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Öğretmeni</label>
                            <select id="df-kabul-ogretmen" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                ${ogretmenOptions}
                            </select>
                        </div>
                    </div>
                `;
            } else if (docType === 'cagri') {
                fields = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Saati</label>
                            <select id="df-cagri-ders-saat" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                <option value="1.DERS SAATİ">1.DERS SAATİ</option>
                                <option value="2.DERS SAATİ">2.DERS SAATİ</option>
                                <option value="3.DERS SAATİ">3.DERS SAATİ</option>
                                <option value="4.DERS SAATİ">4.DERS SAATİ</option>
                                <option value="5.DERS SAATİ">5.DERS SAATİ</option>
                                <option value="6.DERS SAATİ">6.DERS SAATİ</option>
                                <option value="7.DERS SAATİ">7.DERS SAATİ</option>
                                <option value="8.DERS SAATİ">8.DERS SAATİ</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Ders Öğretmeni</label>
                            <select id="df-cagri-ogretmen" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                ${ogretmenOptions}
                            </select>
                        </div>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Çağrı Nedeni</label>
                        <select id="df-cagri-neden" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                            <option value="Öğrencinin Akademik Gelişim Değerlendirmesi">Öğrencinin Akademik Gelişim Değerlendirmesi</option>
                            <option value="Olumsuz Davranış ve Disiplin Görüşmesi">Olumsuz Davranış ve Disiplin Görüşmesi</option>
                            <option value="Devamsızlık Durumu Görüşmesi">Devamsızlık Durumu Görüşmesi</option>
                            <option value="Veli Bilgilendirme ve İş Birliği Toplantısı">Veli Bilgilendirme ve İş Birliği Toplantısı</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">İlgili Birim / Yer</label>
                        <select id="df-cagri-birim" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                            <option value="İdare / Rehberlik">İdare / Rehberlik</option>
                            <option value="Sınıf Rehber Öğretmeni">Sınıf Rehber Öğretmeni</option>
                            <option value="Okul Müdürlüğü">Okul Müdürlüğü</option>
                        </select>
                    </div>
                `;
            } else if (docType === 'veli-izin') {
                fields = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Başlangıç Tarihi</label>
                            <input type="date" id="df-veli-baslangic" class="input-field" value="${today}" style="">
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Bitiş Tarihi</label>
                            <input type="date" id="df-veli-bitis" class="input-field" value="${today}" style="">
                        </div>
                    </div>
                `;
            } else if (docType === 'uyari') {
                fields = `
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Uyarı Sebebi (Olumsuz Davranış)</label>
                        <input type="text" id="df-uyari-davranis" class="input-field" placeholder="Örn: Sınıf içi kurallara uymamakta ısrar etme" style="">
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Sınıf Rehber Öğrt.</label>
                            <select id="df-uyari-sinif-ref" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                ${ogretmenOptions}
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Rehber Öğretmen</label>
                            <select id="df-uyari-ref" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                                ${ogretmenOptions}
                            </select>
                        </div>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--text-secondary); display:block; margin-bottom:0.4rem;">Müdür Yardımcısı</label>
                        <select id="df-uyari-mdr-yrd" class="input-field" style="width:100%; box-sizing:border-box; height:48px; padding:0.5rem 1rem; ">
                            ${idareOptions}
                        </select>
                    </div>
                `;
            }
            
            container.innerHTML = fields;
            
            // Veli İzin Dilekçesi için Onaylayan bölümünü gizle, diğerleri için göster
            const approverSection = document.getElementById('doc-approver-section');
            if (approverSection) {
                if (docType === 'veli-izin') {
                    approverSection.style.setProperty('display', 'none', 'important');
                } else {
                    approverSection.style.setProperty('display', 'flex', 'important');
                }
            }
        }


        async function printDocument() {
            if (!selectedDocStudent) return;
            
            const docType = document.getElementById('doc-type-select').value;
            const dateStr = document.getElementById('doc-current-date').innerText;
            
            let docTypeName = 'Resmi Belge';
            if (docType === 'izin') docTypeName = 'Mazeret İzni';
            else if (docType === 'gec') docTypeName = 'Geç Kağıdı';
            else if (docType === 'kabul') docTypeName = 'Derse Kabul';
            else if (docType === 'cagri') docTypeName = 'Çağrı Pusulası';
            else if (docType === 'veli-izin') docTypeName = 'Veli İzin Dilekçesi';
            else if (docType === 'uyari') docTypeName = 'Yazılı Uyarı';
            
            const formatTurkishDate = (dStr) => {
                if (!dStr) return '';
                const parts = dStr.split('-');
                if (parts.length === 3) return parts[2] + '/' + parts[1] + '/' + parts[0];
                return dStr;
            };

            const isAnonymous = String(selectedDocStudent.no) === 'ADI';

            // Geçmişe kaydetme mantığı (Sadece gerçek öğrenciler için)
            if (!isAnonymous) {
                if (!selectedDocStudent.history) {
                    selectedDocStudent.history = [];
                }
                
                let details = '';
                
                if (docType === 'izin') {
                    const basSaat = document.getElementById('df-izin-baslangic-saat')?.value || '';
                    const bitSaat = document.getElementById('df-izin-bitis-saat')?.value || '';
                    const mazeret = document.getElementById('df-izin-neden')?.value || '';
                    const izinAraligi = (basSaat === bitSaat || bitSaat === 'DERS SAATİ') ? basSaat : `${basSaat} - ${bitSaat}`;
                    details = `${izinAraligi} | Neden: ${mazeret}`;
                } else if (docType === 'gec') {
                    docTypeName = 'Geç Kağıdı';
                    const mazeret = document.getElementById('df-gec-neden')?.value || '';
                    const dersSaat = document.getElementById('df-gec-ders-saat')?.value || '';
                    details = `${dersSaat} | Neden: ${mazeret}`;
                } else if (docType === 'kabul') {
                    docTypeName = 'Derse Kabul';
                    const ogretmen = document.getElementById('df-kabul-ogretmen')?.value || '';
                    const dersSaat = document.getElementById('df-kabul-saat')?.value || '';
                    details = `${dersSaat} | Öğretmen: ${ogretmen}`;
                } else if (docType === 'cagri') {
                    docTypeName = 'Çağrı Pusulası';
                    const dersSaat = document.getElementById('df-cagri-ders-saat')?.value || '';
                    const ogretmen = document.getElementById('df-cagri-ogretmen')?.value || '';
                    const birim = document.getElementById('df-cagri-birim')?.value || '';
                    details = `${dersSaat} | Yer: ${birim} | Öğretmen: ${ogretmen}`;
                } else if (docType === 'veli-izin') {
                    docTypeName = 'Veli İzin Dilekçesi';
                    const basTarih = formatTurkishDate(document.getElementById('df-veli-izin-bas-tarih')?.value || '');
                    const bitTarih = formatTurkishDate(document.getElementById('df-veli-izin-bit-tarih')?.value || '');
                    const mazeret = document.getElementById('df-veli-izin-neden')?.value || '';
                    details = `${basTarih} - ${bitTarih} | Neden: ${mazeret}`;
                } else if (docType === 'uyari') {
                    docTypeName = 'Yazılı Uyarı';
                    const davranis = document.getElementById('df-uyari-davranis')?.value || '';
                    details = `Sebep: ${davranis}`;
                }
                
                selectedDocStudent.history.unshift({
                    tarih: dateStr,
                    tur: docTypeName,
                    detay: details
                });

                if (supabaseClient) {
                    try {
                        await supabaseClient.from('document_history').insert({
                            student_no: parseInt(selectedDocStudent.no, 10),
                            tarih: dateStr,
                            tur: docTypeName,
                            detay: details
                        });
                    } catch (err) {
                        console.error("Supabase print log insert failed:", err);
                    }
                }
                
                persistSchoolData();
            }
            
            const printArea = document.getElementById('print-section');
            let nameStr = '';
            let noStr = '';
            let classStr = '';
            
            if (isAnonymous) {
                nameStr = '................................................';
                noStr = '........................';
                classStr = '........................';
            } else {
                nameStr = (selectedDocStudent.ad || '') + ' ' + (selectedDocStudent.soyad || '');
                noStr = selectedDocStudent.no || '-';
                
                classStr = selectedDocStudent.snf ? (selectedDocStudent.snf + (selectedDocStudent.sube ? '/' + selectedDocStudent.sube : '')) : '-';
            }
            
            let docHTML = '';

            // Varsayılan İdare/Okul Adı
            const schoolName = "CEYLANPINAR FEN LİSESİ MÜDÜRLÜĞÜ";
            const mdr_ad = document.getElementById('doc-approver-name')?.value || ((schoolData && schoolData.idare && schoolData.idare[0]) ? schoolData.idare[0].ad_soyad : "Hüseyin ÇITIRKE");
            const mdr_unvan = document.getElementById('doc-approver-title')?.value || ((schoolData && schoolData.idare && schoolData.idare[0]) ? schoolData.idare[0].unvan : "Okul Müdürü");

            if (docType === 'izin') {
                const basSaat = document.getElementById('df-izin-baslangic-saat').value;
                const bitSaat = document.getElementById('df-izin-bitis-saat').value;
                const mazeret = document.getElementById('df-izin-neden').value;
                const izinAraligi = (basSaat === bitSaat || bitSaat === 'DERS SAATİ') ? basSaat : `${basSaat} ile ${bitSaat}`;
                
                docHTML = `
                    <div class="school-doc-paper a6-paper">
                        <div class="school-doc-header" style="border-bottom:2px double #000; padding-bottom:0.3rem; margin-bottom:0; text-align:center;">
                            <h2 style="font-size:0.88rem; font-weight:bold; margin:0; text-transform:uppercase; white-space:nowrap;">${schoolName}</h2>
                        </div>
                        <div style="display:flex; justify-content:flex-end; font-size:0.8rem; font-weight:bold; margin:0; width:100%;">
                            <span style="border-bottom:1px dotted #000; padding-bottom:2px; white-space:nowrap;">Tarih: ${dateStr}</span>
                        </div>
                        <div style="text-align:center; font-size:0.95rem; font-weight:bold; margin:0; text-transform:uppercase;">ÖĞRENCİ İZİN KAĞIDI</div>
                        <div class="school-doc-body" style="line-height:1.45; font-size:0.8rem; margin:0; text-align:left;">
                            ADI SOYADI: <strong>${nameStr}</strong><br>
                            NUMARASI: <strong>${noStr}</strong><br>
                            SINIF/ŞUBE: <strong>${classStr}</strong><br>
                            İZİN MAZERETİ: <strong>${mazeret}</strong><br><br>
                            İZİN SÜRESİ: <strong>${dateStr}</strong> tarihinde, <strong>${izinAraligi}</strong> arasında
                        </div>
                        <div style="font-size:0.8rem; line-height:1.4; text-align:justify; margin:0;">
                            Yukarıda bilgileri yazılı öğrencinin mazereti uygun görüldüğünden belirtilen sürece izinli sayılması hususunda gereğini rica ederim.
                        </div>
                        <div class="school-doc-footer" style="display:flex; justify-content:flex-end; margin-top:0; font-size:0.8rem;">
                            <div style="text-align:center; min-width:180px;">
                                <br>
                                <strong>${mdr_ad}</strong><br>
                                ${mdr_unvan}
                            </div>
                        </div>
                    </div>
                `;
            } else if (docType === 'gec') {
                const mazeret = document.getElementById('df-gec-neden').value;
                const ogretmen = document.getElementById('df-gec-ogretmen').value || 'Nöbetçi Öğretmen';
                const dersSaati = document.getElementById('df-gec-ders-saat')?.value || '';
                
                docHTML = `
                    <div class="school-doc-paper a6-paper">
                        <div class="school-doc-header" style="border-bottom:2px double #000; padding-bottom:0.3rem; margin-bottom:0; text-align:center;">
                            <h2 style="font-size:0.88rem; font-weight:bold; margin:0; text-transform:uppercase; white-space:nowrap;">${schoolName}</h2>
                        </div>
                        <div style="display:flex; justify-content:flex-end; font-size:0.8rem; font-weight:bold; margin:0; width:100%;">
                            <span style="border-bottom:1px dotted #000; padding-bottom:2px; white-space:nowrap;">Tarih: ${dateStr}</span>
                        </div>
                        <div style="text-align:center; font-size:0.95rem; font-weight:bold; margin:0; text-transform:uppercase;">ÖĞRENCİ GEÇ KAĞIDI</div>
                        <div class="school-doc-body" style="line-height:1.45; font-size:0.8rem; margin:0; text-align:left;">
                            ADI SOYADI: <strong>${nameStr}</strong><br>
                            NUMARASI: <strong>${noStr}</strong><br>
                            SINIF/ŞUBE: <strong>${classStr}</strong><br>
                            DERS SAATİ: <strong>${dersSaati}</strong><br><br>
                            GECİKME SEBEBİ: <strong>${mazeret}</strong>
                        </div>
                        <div style="font-size:0.8rem; line-height:1.4; text-align:justify; margin:0;">
                            <strong>Sayın ${ogretmen}</strong><br>
                            Yukarıda bilgileri yazılı öğrenci mazeretli olarak gecikmiştir. Öğrencinin derse kabulünü ve bu tezkerenin yoklama defteri arasına konulmasını rica ederim.
                        </div>
                        <div class="school-doc-footer" style="display:flex; justify-content:space-between; margin-top:0; font-size:0.8rem;">
                            <div style="text-align:left; font-size:0.75rem; line-height:1.3; align-self:flex-end;">
                                Yoklama fişine işlendi.<br>
                                Öğretmenin İmzası
                            </div>
                            <div style="text-align:center; min-width:180px;">
                                <br>
                                <strong>${mdr_ad}</strong><br>
                                ${mdr_unvan}
                            </div>
                        </div>
                    </div>
                `;
            } else if (docType === 'kabul') {
                const dersSaat = document.getElementById('df-kabul-saat').value;
                const ogretmen = document.getElementById('df-kabul-ogretmen').value || 'Nöbetçi Öğretmen';
                
                docHTML = `
                    <div class="school-doc-paper a6-paper">
                        <div class="school-doc-header" style="border-bottom:2px double #000; padding-bottom:0.3rem; margin-bottom:0; text-align:center;">
                            <h2 style="font-size:0.88rem; font-weight:bold; margin:0; text-transform:uppercase; white-space:nowrap;">${schoolName}</h2>
                        </div>
                        <div style="display:flex; justify-content:flex-end; font-size:0.8rem; font-weight:bold; margin:0; width:100%;">
                            <span style="border-bottom:1px dotted #000; padding-bottom:2px; white-space:nowrap;">Tarih: ${dateStr}</span>
                        </div>
                        <div style="text-align:center; font-size:0.95rem; font-weight:bold; margin:0; text-transform:uppercase;">DERSE KABUL KAĞIDI</div>
                        <div class="school-doc-body" style="line-height:1.45; font-size:0.8rem; margin:0; text-align:left;">
                            ADI SOYADI: <strong>${nameStr}</strong><br>
                            NUMARASI: <strong>${noStr}</strong><br>
                            SINIF/ŞUBE: <strong>${classStr}</strong><br>
                            DERS SAATİ: <strong>${dersSaat}</strong>
                        </div>
                        <div style="font-size:0.8rem; line-height:1.4; text-align:justify; margin:0;">
                            <strong>Sayın ${ogretmen}</strong><br>
                            Yukarıda bilgileri yazılı öğrencinin derse kabulünü ve bu tezkerenin yoklama defteri arasına konulmasını rica ederim.
                        </div>
                        <div class="school-doc-footer" style="display:flex; justify-content:flex-end; margin-top:0; font-size:0.8rem;">
                            <div style="text-align:center; min-width:180px;">
                                <br>
                                <strong>${mdr_ad}</strong><br>
                                ${mdr_unvan}
                            </div>
                        </div>
                    </div>
                `;
            } else if (docType === 'cagri') {
                const birim = document.getElementById('df-cagri-birim').value;
                const neden = document.getElementById('df-cagri-neden').value;
                const dersSaat = document.getElementById('df-cagri-ders-saat').value;
                const ogretmen = document.getElementById('df-cagri-ogretmen').value || 'Nöbetçi Öğretmen';
                
                docHTML = `
                    <div class="school-doc-paper a6-paper">
                        <div class="school-doc-header" style="border-bottom:2px double #000; padding-bottom:0.3rem; margin-bottom:0; text-align:center;">
                            <h2 style="font-size:0.88rem; font-weight:bold; margin:0; text-transform:uppercase; white-space:nowrap;">${schoolName}</h2>
                        </div>
                        <div style="display:flex; justify-content:flex-end; font-size:0.8rem; font-weight:bold; margin:0; width:100%;">
                            <span style="border-bottom:1px dotted #000; padding-bottom:2px; white-space:nowrap;">Tarih: ${dateStr}</span>
                        </div>
                        <div style="text-align:center; font-size:0.95rem; font-weight:bold; margin:0; text-transform:uppercase;">ÇAĞRI PUSULASI</div>
                        <div class="school-doc-body" style="line-height:1.45; font-size:0.8rem; margin:0; text-align:left;">
                            ADI SOYADI: <strong>${nameStr}</strong><br>
                            NUMARASI: <strong>${noStr}</strong><br>
                            SINIF/ŞUBE: <strong>${classStr}</strong><br>
                            DERS SAATİ: <strong>${dersSaat}</strong><br><br>
                            ÇAĞRILAN YER: <strong>${birim}</strong><br>
                            ÇAĞRI NEDENİ: <strong>${neden}</strong>
                        </div>
                        <div style="font-size:0.8rem; line-height:1.4; text-align:justify; margin:0;">
                            <strong>Sayın ${ogretmen}</strong><br>
                            Yukarıda bilgileri yazılı öğrencinin tezkereyi aldıktan sonra derhal belirtilen birime gelmesini rica ederim.
                        </div>
                        <div class="school-doc-footer" style="display:flex; justify-content:flex-end; margin-top:0; font-size:0.8rem;">
                            <div style="text-align:center; min-width:180px;">
                                <br>
                                <strong>${mdr_ad}</strong><br>
                                ${mdr_unvan}
                            </div>
                        </div>
                    </div>
                `;
            } else if (docType === 'veli-izin') {
                const bas = formatTurkishDate(document.getElementById('df-veli-baslangic').value);
                const bit = formatTurkishDate(document.getElementById('df-veli-bitis').value);
                
                docHTML = `
                    <div class="school-doc-paper a4-paper" style="font-family:'Times New Roman', serif; max-width:650px;">
                        <div class="school-doc-header" style="border:none; margin-bottom:2rem;">
                            <h2>CEYLANPINAR FEN LİSESİ MÜDÜRLÜĞÜNE</h2>
                        </div>
                        <div class="school-doc-body" style="font-size:0.95rem; line-height:1.8; text-align:justify;">
                            Velisi bulunduğum okulunuz <strong>${classStr}</strong> sınıfı, <strong>${noStr}</strong> numaralı <strong>${nameStr}</strong> isimli öğrencim <strong>${bas}</strong> ile <strong>${bit}</strong> tarihleri arasında bilgim dahilinde mazeretinden ötürü okula gelmemiştir.<br><br>
                            Öğrencimin belirtilen tarihlerde izinli sayılması hususunda gereğini arz ederim.
                        </div>
                        <div style="margin-top:2rem; display:flex; justify-content:space-between; font-size:0.9rem;">
                            <div>
                                <strong>ADRES:</strong><br>
                                <span style="border-bottom:1px dotted #000; width:220px; display:inline-block; height:20px;"></span><br>
                                <span style="border-bottom:1px dotted #000; width:220px; display:inline-block; height:20px;"></span><br>
                                <strong>TEL:</strong> <span style="border-bottom:1px dotted #000; width:170px; display:inline-block; height:20px;"></span>
                            </div>
                            <div style="text-align:center; min-width:180px;">
                                <div>..../..../202...</div><br>
                                <strong>VELİ</strong><br><br>
                                <span>ADI SOYADI: .............................</span><br><br>
                                <span>İMZA: .............................</span>
                            </div>
                        </div>
                    </div>
                `;
            } else if (docType === 'uyari') {
                const davranis = document.getElementById('df-uyari-davranis').value || '';
                const sinif_ref = document.getElementById('df-uyari-sinif-ref').value || 'Sınıf Rehber Öğretmeni';
                const ref = document.getElementById('df-uyari-ref').value || 'Rehber Öğretmen';
                const mdr_yrd = document.getElementById('df-uyari-mdr-yrd').value || 'Müdür Yardımcısı';
                
                docHTML = `
                    <div class="school-doc-paper a4-paper" style="display:flex; flex-direction:column; justify-content:space-between; height:260mm; padding:20mm; box-sizing:border-box;">
                        <div style="display:flex; flex-direction:column; gap:1.25rem; font-family:'Inter', 'Outfit', sans-serif;">
                            <!-- Header -->
                            <div style="text-align:center; line-height:1.5; font-size:1.15rem; font-weight:bold; text-transform:uppercase;">
                                T.C.<br>
                                CEYLANPINAR KAYMAKAMLIĞI<br>
                                CEYLANPINAR FEN LİSESİ
                            </div>
                            
                            <!-- Title -->
                            <div style="text-align:center; font-size:1.35rem; font-weight:bold; margin-top:1.2rem; margin-bottom:1.2rem; text-transform:uppercase;">
                                YAZILI UYARI BELGESİ
                            </div>
                            
                            <!-- Student Info -->
                            <div style="font-size:1rem; line-height:1.8; margin-bottom:0.8rem;">
                                ADI SOYADI: <strong>${nameStr}</strong><br>
                                NUMARASI: <strong>${noStr}</strong><br>
                                SINIF/ŞUBE: <strong>${classStr}</strong>
                            </div>
                            
                            <!-- Paragraph 1 -->
                            <div style="font-size:0.95rem; line-height:1.6; text-align:justify; text-indent:2rem;">
                                Ortaöğretim Kurumları Yönetmeliğinin 157. Maddesinin 7. Fıkrasının a bendi gereği; yapılan toplantıda; Öğrencinin davranışlarında kusurlu olduğu, öğrenciden beklenen olumlu davranışın neler olabileceği anlatılmış, olumsuz davranışlarının devamı hâlinde kendisine uygulanabilecek yaptırımlar konusunda öğrenci yazılı olarak uyarılmıştır. Öğrencinin olumsuz davranışları sürdürmesi hâlinde velisinin okula davet edileceği, olumsuz davranışları ve uygulanabilecek yaptırımlar hakkında velisinin bilgilendirileceği belirtilmiştir.
                            </div>
                            
                            <!-- Paragraph 2 -->
                            <div style="font-size:0.95rem; line-height:1.6; text-align:justify; text-indent:2rem;">
                                Öğrenciye; disiplin cezasını gerektiren davranış ve fiillerin niteliklerine göre;
                            </div>
                            
                            <!-- Bullet list -->
                            <div style="font-size:0.95rem; line-height:1.6; padding-left:4rem;">
                                Kınama,<br>
                                Okuldan kısa süreli uzaklaştırma,<br>
                                Okul değiştirme,<br>
                                Örgün eğitim dışına çıkarma,<br><br>
                                Cezalarından birinin verilebileceği ayrıntılı olarak anlatılmıştır.
                            </div>
                            
                            <!-- Paragraph 3 -->
                            <div style="font-size:0.95rem; line-height:1.6; text-align:justify; text-indent:2rem;">
                                Öğrenci, yapılan bu sözlü ve yazılı uyarıları dikkate alacağını, olumsuz davranışın tekrarı hâlinde kendisi hakkında yönetmelikte belirtilen gerekli disiplin işlemini kabul edeceğini taahhüt etmiştir.
                            </div>
                            
                            <!-- Reason -->
                            <div style="font-size:1rem; font-weight:bold; margin-top:0.8rem;">
                                ÖĞRENCİNİN YAZILI UYARI SEBEBİ: <span style="font-weight:normal; text-decoration:underline;">${davranis}</span>
                            </div>
                        </div>
                        
                        <!-- Footer Signatures (4 Columns with names above titles) -->
                        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:0.5rem; text-align:center; font-size:0.82rem; margin-top:2rem; width:100%; font-family:'Inter', 'Outfit', sans-serif;">
                            <div>
                                <br><br><br>
                                <span>${sinif_ref}</span><br>
                                <strong>SINIF REHBER ÖĞRT.</strong>
                            </div>
                            <div>
                                <br><br><br>
                                <span>${ref}</span><br>
                                <strong>REHBER ÖĞRETMEN</strong>
                            </div>
                            <div>
                                <br><br><br>
                                <span>${mdr_yrd}</span><br>
                                <strong>İLGİLİ MÜDÜR YRD.</strong>
                            </div>
                            <div>
                                <br><br><br>
                                <span>${mdr_ad}</span><br>
                                <strong>${mdr_unvan.toLocaleUpperCase('tr-TR')}</strong>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            printArea.innerHTML = docHTML;
            document.body.classList.add('print-doc');
            
            const originalTitle = document.title;
            const pdfStudentName = isAnonymous ? 'İsimsiz' : ((selectedDocStudent.ad || '') + ' ' + (selectedDocStudent.soyad || '')).trim();
            const fileDateStr = dateStr.replace(/\//g, '.');
            document.title = `${docTypeName} - ${pdfStudentName} - ${fileDateStr}`;
            
            window.print();
            
            document.title = originalTitle;
            document.body.classList.remove('print-doc');
            closeDocumentModal();
        }


        function persistSchoolData() {
            // Cloud-only yapıda yerel depolama kullanılmaz
        }

        let isLoadedFromCloud = false;

        async function loadSchoolData(forceReload = false) {
            if (isLoadedFromCloud && !forceReload) return;

            if (supabaseClient) {
                try {
                    // 15 saniyelik zaman aşımı tanımlayalım
                    const timeoutPromise = new Promise((_, reject) => 
                        setTimeout(() => reject(new Error("Supabase bağlantı zaman aşımı")), 15000)
                    );

                    // Eşzamanlı sorguları tek bir promise ile birleştirelim
                    const fetchPromise = Promise.all([
                        supabaseClient.from('students').select('*').order('no', { ascending: true }),
                        supabaseClient.from('staff').select('*').order('id', { ascending: true }),
                        supabaseClient.from('document_history').select('*').order('created_at', { ascending: false })
                    ]);

                    // Sorgular ile zaman aşımını yarıştıralım
                    const [resOgr, resStaff, resHist] = await Promise.race([fetchPromise, timeoutPromise]);
                    const { data: students, error: errOgr } = resOgr;
                    const { data: staff, error: errStaff } = resStaff;
                    const { data: history, error: errHist } = resHist;

                    if (!errOgr && !errStaff && !errHist) {
                        schoolData = {
                            ogrenci: (students || []).map(s => ({
                                no: s.no,
                                ad: s.ad,
                                soyad: s.soyad,
                                snf: s.snf,
                                sube: s.sube || '',
                                history: (history || []).filter(h => String(h.student_no) === String(s.no)).map(h => ({
                                    id: h.id,
                                    tarih: h.tarih,
                                    tur: h.tur,
                                    detay: h.detay || ''
                                }))
                            })),
                            ogretmen: (staff || []).filter(st => st.role === 'ogretmen').map(st => ({
                                id: String(st.id),
                                ad_soyad: st.ad_soyad,
                                unvan: st.unvan
                            })),
                            idare: (staff || []).filter(st => st.role === 'idare').map(st => ({
                                id: String(st.id),
                                ad_soyad: st.ad_soyad,
                                unvan: st.unvan
                            }))
                        };
                        updateDbStatusBadge(true);
                        isLoadedFromCloud = true;
                        console.log("School data loaded successfully from Supabase!");
                        return;
                    } else {
                        console.error("Supabase load query errors:", errOgr, errStaff, errHist);
                    }
                } catch(e) {
                    console.error("Supabase load exception:", e);
                }
            }

            // Bağlantı başarısız veya bulunamadı ise kırmızı ışık yak
            updateDbStatusBadge(false);
            
            // Çevrimdışı / Bağlantı kesildi modunda boş nesnelerle başlatıp arayüzün patlamasını önleyelim
            schoolData = {
                ogrenci: [],
                ogretmen: [],
                idare: []
            };
            isLoadedFromCloud = false;
        }

function showSchoolManagementView() {
            document.body.classList.remove('portal-mode');
            document.getElementById('app-container').classList.add('no-sidebar');

            document.getElementById('selection-screen').style.display = 'none';
            document.getElementById('student-hub').style.display = 'none';
            document.getElementById('teacher-hub').style.display = 'none';
            document.getElementById('teacher-analysis-view').style.display = 'none';
            document.getElementById('school-management-view').style.display = 'block';

            document.getElementById('logout-btn').style.display = 'inline-flex';
            document.getElementById('header-logo-section').style.display = 'flex';
            document.getElementById('header-title').innerText = 'Ceylanpınar Fen Lisesi';
            document.getElementById('header-subtitle').innerText = 'Okul Yönetim Sistemi';
            document.getElementById('mobile-nav-analysis').style.setProperty('display', 'none', 'important');

            // Ayarlar dişlisini sadece müdür (admin) rolü için görünür yapalım
            const userRole = sessionStorage.getItem('user_role') || 'student';
            const settingsBtn = document.getElementById('school-settings-btn');
            if (settingsBtn) {
                settingsBtn.style.display = (userRole === 'admin') ? 'inline-flex' : 'none';
            }

            // Supabase'den güncel verileri asenkron yükleyelim
            loadSchoolData().then(() => {
                document.getElementById('school-stat-ogrenci').innerText = schoolData.ogrenci.length;
                document.getElementById('school-stat-ogretmen').innerText = schoolData.ogretmen.length;
                document.getElementById('school-stat-idare').innerText = schoolData.idare.length;

                switchSchoolTab('ogrenci');
            });
        }

        function switchSchoolTab(tab) {
            currentSchoolTab = tab;
            ['ogrenci', 'ogretmen', 'idare'].forEach(t => {
                const btn = document.getElementById('school-tab-' + t);
                if (!btn) return;
                if (t === tab) {
                    btn.style.background = 'var(--accent-gradient)';
                    btn.style.color = '#fff';
                } else {
                    btn.style.background = 'transparent';
                    btn.style.color = 'var(--text-secondary)';
                }
            });
            const s = document.getElementById('school-search-input');
            if (s) s.value = '';
            renderSchoolTable();
        }

        function renderSchoolTable() {
            if (!schoolData) return;
            const query = (document.getElementById('school-search-input')?.value || '').toLowerCase().trim();
            let records = (schoolData[currentSchoolTab] || []).slice();

            const role = sessionStorage.getItem('user_role') || 'student';
            const isAdmin = (role === 'admin');

            if (query) {
                const lowercaseQuery = query.toLocaleLowerCase('tr-TR');
                records = records.filter(r => {
                    // Ad ve soyadı birleştirerek tam isimle aramayı destekle
                    const fullName = ((r.ad || '') + ' ' + (r.soyad || '') + ' ' + (r.ad_soyad || '')).toLocaleLowerCase('tr-TR');
                    const otherFields = Object.values(r).map(v => String(v || '').toLocaleLowerCase('tr-TR'));
                    return fullName.includes(lowercaseQuery) || otherFields.some(f => f.includes(lowercaseQuery));
                });
            }

            const tbody = document.getElementById('school-table-body');
            const footer = document.getElementById('school-table-footer');
            if (!tbody) return;

            if (records.length === 0) {
                tbody.innerHTML = '<div style="padding:3rem; text-align:center; color:var(--text-secondary);"><p style="font-size:1rem;">Kayıt bulunamadı.</p></div>';
                footer.innerText = '0 kayıt';
                return;
            }

            let thead = '', rows = '';

            if (currentSchoolTab === 'ogrenci') {
                thead = '<tr style="background:var(--bg-page); border-bottom:2px solid var(--border-color);"><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">No</th><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Ad Soyad</th><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Sınıf/Şube</th><th style="padding:0.75rem 1rem; text-align:center; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">İşlem</th></tr>';
                
                // İsimsiz Belge Üretme Satırını En Üste Sabitleyelim
                const anonBtnClass = 'btn-action btn-action-anon';
                const anonActionButtons = `<button onclick="openDocumentModal('ADI')" class="${anonBtnClass}"><i data-lucide="file-text" size="13"></i>İsimsiz Belge Üret</button>`;
                rows += `<tr class="school-table-row" style="background:rgba(239, 68, 68, 0.03); border-bottom:1px solid var(--border-color);"><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.8rem;">-</td><td style="padding:0.7rem 1rem; font-weight:600; color:var(--text-primary);">İSİMSİZ BELGE ÜRETİMİ</td><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.85rem;">-</td><td style="padding:0.7rem 1rem; text-align:center;">${anonActionButtons}</td></tr>`;

                records.forEach(r => {
                    // Veritabanındaki eski "ADI" satırını (varsa) atlayalım
                    if (String(r.no) === 'ADI') return;
                    
                    const btnClass = 'btn-action btn-action-print';
                    const btnIcon = 'printer';
                    const btnText = 'Belge Üret';
                    let actionButtons = `<button onclick="openDocumentModal('${r.no||''}')" class="${btnClass}"><i data-lucide="${btnIcon}" size="13"></i>${btnText}</button>`;
                    if (isAdmin) {
                        actionButtons += `<button onclick="openSchoolModal('${r.no||''}')" class="btn-action btn-action-edit"><i data-lucide="edit-2" size="13"></i>Düzenle</button><button onclick="deleteSchoolRecord('${r.no||''}','ogrenci')" class="btn-action btn-action-delete"><i data-lucide="trash-2" size="13"></i>Sil</button>`;
                    }
                    
                    // Sınıf ve Şube bilgilerini birleştirelim
                    const displayClass = r.snf ? (r.snf + (r.sube ? '/' + r.sube : '')) : '-';
                    
                    rows += `<tr class="school-table-row"><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.8rem;">${r.no||'-'}</td><td style="padding:0.7rem 1rem; font-weight:500; color:var(--text-primary);">${r.ad||''} ${r.soyad||''}</td><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.85rem;">${displayClass}</td><td style="padding:0.7rem 1rem; text-align:center;">${actionButtons}</td></tr>`;
                });
            } else if (currentSchoolTab === 'ogretmen') {
                thead = '<tr style="background:var(--bg-page); border-bottom:2px solid var(--border-color);"><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">ID</th><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Ad Soyad</th><th style="padding:0.75rem 1rem; text-align:center; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">İşlem</th></tr>';
                records.forEach(r => {
                    const rec = JSON.stringify(r).replace(/'/g, "&#39;");
                    let actionButtons = '';
                    if (isAdmin) {
                        actionButtons += `<button onclick="openSchoolModal('${r.id||''}')" class="btn-action btn-action-edit"><i data-lucide="edit-2" size="13"></i>Düzenle</button><button onclick="deleteSchoolRecord('${r.id||''}','ogretmen')" class="btn-action btn-action-delete"><i data-lucide="trash-2" size="13"></i>Sil</button>`;
                    } else {
                        actionButtons += '';
                    }
                    rows += `<tr class="school-table-row"><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.8rem;">${r.id||'-'}</td><td style="padding:0.7rem 1rem; font-weight:500; color:var(--text-primary);">${r.ad_soyad||''}</td><td style="padding:0.7rem 1rem; text-align:center;">${actionButtons}</td></tr>`;
                });
            } else {
                thead = '<tr style="background:var(--bg-page); border-bottom:2px solid var(--border-color);"><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">ID</th><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Ad Soyad</th><th style="padding:0.75rem 1rem; text-align:left; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Unvan</th><th style="padding:0.75rem 1rem; text-align:center; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">İşlem</th></tr>';
                records.forEach(r => {
                    const rec = JSON.stringify(r).replace(/'/g, "&#39;");
                    let actionButtons = '';
                    if (isAdmin) {
                        actionButtons += `<button onclick="openSchoolModal('${r.id||''}')" class="btn-action btn-action-edit"><i data-lucide="edit-2" size="13"></i>Düzenle</button><button onclick="deleteSchoolRecord('${r.id||''}','idare')" class="btn-action btn-action-delete"><i data-lucide="trash-2" size="13"></i>Sil</button>`;
                    } else {
                        actionButtons += '';
                    }
                    rows += `<tr class="school-table-row"><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.8rem;">${r.id||'-'}</td><td style="padding:0.7rem 1rem; font-weight:500; color:var(--text-primary);">${r.ad_soyad||''}</td><td style="padding:0.7rem 1rem; color:var(--text-secondary); font-size:0.85rem;">${r.unvan||'-'}</td><td style="padding:0.7rem 1rem; text-align:center;">${actionButtons}</td></tr>`;
                });
            }

            let tfoot = '';
            if (isAdmin && records.length > 0) {
                const colspan = (currentSchoolTab === 'ogrenci') ? 3 : 2;
                tfoot = `<tfoot><tr style="background:var(--bg-page); border-top:2px solid var(--border-color);"><td colspan="${colspan}" style="padding:0.75rem 1rem; font-weight:600; color:var(--text-secondary); font-size:0.8rem;">Toplam ${records.length} kayıt listelendi</td><td style="padding:0.75rem 1rem; text-align:center;"><button onclick="clearAllSchoolTabRecords()" style="background:none; border:1px solid #fee2e2; border-radius:6px; padding:0.25rem 0.65rem; cursor:pointer; color:#ef4444; font-size:0.78rem; font-weight:600; transition:all 0.15s;" onmouseover="this.style.background='#fee2e2'" onmouseout="this.style.background=''">Tümünü Sil</button></td></tr></tfoot>`;
            }
            tbody.innerHTML = '<table style="width:100%; border-collapse:collapse; font-size:0.875rem;"><thead>' + thead + '</thead><tbody>' + rows + '</tbody>' + tfoot + '</table>';
            footer.innerText = records.length + ' kayıt gösteriliyor (toplam ' + schoolData[currentSchoolTab].length + ')';
            if (window.lucide) lucide.createIcons();
        }

        function openSchoolModal(recordOrId) {
            let record = null;
            if (recordOrId && typeof recordOrId !== 'object') {
                const searchTab = currentSchoolTab;
                record = schoolData[searchTab].find(r => String(r.no || r.id) === String(recordOrId));
            } else {
                record = recordOrId;
            }
            schoolEditId = record ? (record.no || record.id || null) : null;
            document.getElementById('school-modal-title').innerText = record ? 'Kaydı Düzenle' : 'Yeni Kayıt Ekle';

            let fields = '';
            if (currentSchoolTab === 'ogrenci') {
                fields = '<div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Öğrenci No</label><input id="mf-no" class="input-field" value="' + (record?record.no||'':'') + '" placeholder="Örn: 1001"></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;"><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Ad</label><input id="mf-ad" class="input-field" value="' + (record?record.ad||'':'') + '" placeholder="Ad"></div><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Soyad</label><input id="mf-soyad" class="input-field" value="' + (record?record.soyad||'':'') + '" placeholder="Soyad"></div></div><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Sınıf</label><input id="mf-snf" class="input-field" value="' + (record?record.snf||'':'') + '" placeholder="Örn: 10-A"></div>';
            } else if (currentSchoolTab === 'ogretmen') {
                fields = '<div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">ID</label><input id="mf-id" class="input-field" value="' + (record?record.id||'':'') + '" placeholder="Sıra no"></div><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Ad Soyad</label><input id="mf-ad_soyad" class="input-field" value="' + (record?record.ad_soyad||'':'') + '" placeholder="Ad Soyad"></div>';
            } else {
                fields = '<div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">ID</label><input id="mf-id" class="input-field" value="' + (record?record.id||'':'') + '" placeholder="Sıra no"></div><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Ad Soyad</label><input id="mf-ad_soyad" class="input-field" value="' + (record?record.ad_soyad||'':'') + '" placeholder="Ad Soyad"></div><div><label style="font-size:0.8rem;font-weight:600;color:var(--text-secondary);display:block;margin-bottom:0.4rem;">Unvan</label><input id="mf-unvan" class="input-field" value="' + (record?record.unvan||'':'') + '" placeholder="Örn: Müdür"></div>';
            }

            document.getElementById('school-modal-body').innerHTML = fields;
            document.getElementById('school-modal').style.display = 'flex';
        }

        function closeSchoolModal() {
            document.getElementById('school-modal').style.display = 'none';
            schoolEditId = null;
        }

        async function saveSchoolRecord() {
            if (!supabaseClient) { alert('Bulut bağlantısı yok! İşlem gerçekleştirilemedi.'); return; }
            if (!schoolData) return;

            if (currentSchoolTab === 'ogrenci') {
                const no = parseInt((document.getElementById('mf-no')?.value || '').trim(), 10);
                const ad = (document.getElementById('mf-ad')?.value || '').trim();
                const soyad = (document.getElementById('mf-soyad')?.value || '').trim();
                const snf = (document.getElementById('mf-snf')?.value || '').trim();
                if (isNaN(no) || !ad || !soyad) { alert('No (sayısal), Ad ve Soyad zorunludur!'); return; }
                
                if (supabaseClient) {
                    if (schoolEditId) {
                        // Numara değiştiyse foreign key tutarlılığı için sicil kayıtlarını da güncelliyoruz
                        if (String(schoolEditId) !== String(no)) {
                            await supabaseClient.from('document_history').update({ student_no: no }).eq('student_no', schoolEditId);
                        }
                        const { error } = await supabaseClient.from('students').update({ no, ad, soyad, snf }).eq('no', schoolEditId);
                        if (error) { alert('Güncelleme hatası: ' + error.message); return; }
                    } else {
                        const { error } = await supabaseClient.from('students').insert({ no, ad, soyad, snf });
                        if (error) { 
                            if (error.code === '23505') alert('Bu numara zaten kayıtlı!');
                            else alert('Ekleme hatası: ' + error.message);
                            return; 
                        }
                    }
                } else {
                    // Local fallback
                    if (schoolEditId) {
                        const idx = schoolData.ogrenci.findIndex(r => String(r.no) === String(schoolEditId));
                        if (idx >= 0) {
                            const existingHistory = schoolData.ogrenci[idx].history || [];
                            schoolData.ogrenci[idx] = {no, ad, soyad, snf, history: existingHistory};
                        }
                    } else {
                        if (schoolData.ogrenci.find(r => String(r.no) === String(no))) { alert('Bu numara zaten kayıtlı!'); return; }
                        schoolData.ogrenci.push({no, ad, soyad, snf});
                    }
                }
            } else if (currentSchoolTab === 'ogretmen') {
                const id = (document.getElementById('mf-id')?.value || '').trim();
                const ad_soyad = (document.getElementById('mf-ad_soyad')?.value || '').trim();
                if (!ad_soyad) { alert('Ad Soyad zorunludur!'); return; }
                
                if (supabaseClient) {
                    if (schoolEditId) {
                        await supabaseClient.from('staff').update({ ad_soyad, unvan: 'Rehber Öğretmen' }).eq('id', schoolEditId);
                    } else {
                        await supabaseClient.from('staff').insert({ ad_soyad, unvan: 'Rehber Öğretmen', role: 'ogretmen' });
                    }
                } else {
                    // Local fallback
                    if (schoolEditId) {
                        const idx = schoolData.ogretmen.findIndex(r => String(r.id) === String(schoolEditId));
                        if (idx >= 0) schoolData.ogretmen[idx] = {id, ad_soyad};
                    } else {
                        schoolData.ogretmen.push({id: id || String(schoolData.ogretmen.length + 1), ad_soyad});
                    }
                }
            } else {
                const id = (document.getElementById('mf-id')?.value || '').trim();
                const ad_soyad = (document.getElementById('mf-ad_soyad')?.value || '').trim();
                const unvan = (document.getElementById('mf-unvan')?.value || '').trim();
                if (!ad_soyad) { alert('Ad Soyad zorunludur!'); return; }
                
                if (supabaseClient) {
                    if (schoolEditId) {
                        await supabaseClient.from('staff').update({ ad_soyad, unvan }).eq('id', schoolEditId).eq('role', currentSchoolTab);
                    } else {
                        await supabaseClient.from('staff').insert({ ad_soyad, unvan, role: currentSchoolTab });
                    }
                } else {
                    // Local fallback
                    if (schoolEditId) {
                        const idx = schoolData.idare.findIndex(r => String(r.id) === String(schoolEditId));
                        if (idx >= 0) schoolData.idare[idx] = {id, ad_soyad, unvan};
                    } else {
                        schoolData.idare.push({id: id || String(schoolData.idare.length + 1), ad_soyad, unvan});
                    }
                }
            }

            // Yeniden asenkron çekelim ve arayüzü güncelleyelim
            await loadSchoolData(true);
            
            document.getElementById('school-stat-ogrenci').innerText = schoolData.ogrenci.length;
            document.getElementById('school-stat-ogretmen').innerText = schoolData.ogretmen.length;
            document.getElementById('school-stat-idare').innerText = schoolData.idare.length;

            closeSchoolModal();
            renderSchoolTable();
            persistSchoolData();
            showToast(schoolEditId ? 'Kayıt güncellendi!' : 'Yeni kayıt eklendi!');
        }

        function clearAllSchoolTabRecords() {
            if (!supabaseClient) { alert('Bulut bağlantısı yok! İşlem gerçekleştirilemedi.'); return; }
            let tabLabel = "öğrencileri";
                            if (currentSchoolTab === 'ogretmen') tabLabel = "öğretmenleri";
                            if (currentSchoolTab === 'idare') tabLabel = "idarecileri";

                            if (!confirm(`Mevcut listedeki tüm ${tabLabel} silmek istediğinize emin misiniz?`)) return;
                            if (!schoolData) return;

                            if (supabaseClient) {
                                if (currentSchoolTab === 'ogrenci') {
                                    supabaseClient.from('document_history').delete().neq('id', 0).then(() => {
                                        supabaseClient.from('students').delete().neq('no', 0).then(() => {
                                            loadSchoolData(true).then(() => {
                                                updateStatsAndTable('Tüm kayıtlar silindi!');
                                            });
                                        });
                                    });
                                    return;
                                } else if (currentSchoolTab === 'ogretmen') {
                                    supabaseClient.from('staff').delete().eq('role', 'ogretmen').then(() => {
                                        loadSchoolData(true).then(() => {
                                            updateStatsAndTable('Tüm kayıtlar silindi!');
                                        });
                                    });
                                    return;
                                } else {
                                    supabaseClient.from('staff').delete().eq('role', 'idare').then(() => {
                                        loadSchoolData(true).then(() => {
                                            updateStatsAndTable('Tüm kayıtlar silindi!');
                                        });
                                    });
                                    return;
                                }
                            } else {
                                // Local fallback
                                schoolData[currentSchoolTab] = [];
                            }

                            updateStatsAndTable('Tüm kayıtlar silindi!');
                        }

                        async function deleteSchoolRecord(id, tab) {
                            if (!supabaseClient) { alert('Bulut bağlantısı yok! İşlem gerçekleştirilemedi.'); return; }
                            if (!confirm('Bu kaydı silmek istediğinizden emin misiniz?')) return;
                            if (!schoolData) return;

                            if (supabaseClient) {
                                if (tab === 'ogrenci') {
                                    await supabaseClient.from('document_history').delete().eq('student_no', id);
                                    await supabaseClient.from('students').delete().eq('no', id);
                                } else {
                                    await supabaseClient.from('staff').delete().eq('id', id).eq('role', tab);
                                }
                            } else {
                                // Local fallback
                                if (tab === 'ogrenci') {
                                    schoolData.ogrenci = schoolData.ogrenci.filter(r => String(r.no) !== String(id));
                                } else if (tab === 'ogretmen') {
                                    schoolData.ogretmen = schoolData.ogretmen.filter(r => String(r.id) !== String(id));
                                } else {
                                    schoolData.idare = schoolData.idare.filter(r => String(r.id) !== String(id));
                                }
                            }

                            await loadSchoolData(true);
                            updateStatsAndTable('Kayıt silindi!');
                        }

                        function updateStatsAndTable(msg) {
                            document.getElementById('school-stat-ogrenci').innerText = schoolData.ogrenci.length;
                            document.getElementById('school-stat-ogretmen').innerText = schoolData.ogretmen.length;
                            document.getElementById('school-stat-idare').innerText = schoolData.idare.length;
                            renderSchoolTable();
                            persistSchoolData();
                            if (msg) showToast(msg);
                        }


        function renderProgressChart(records) {
            const ctx = document.getElementById('progressChart').getContext('2d');
            if (progressChart) {
                progressChart.destroy();
            }

            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(15,23,42,0.08)';
            const textColor = isDark ? '#94a3b8' : '#64748b';

            // Calculate overall average net for each exam across ALL students in the database
            const examAvgsMap = {};
            examDatabase.forEach(rec => {
                if (rec.subjects && rec.subjects.toplam) {
                    if (!examAvgsMap[rec.deneme]) {
                        examAvgsMap[rec.deneme] = { sum: 0, count: 0 };
                    }
                    examAvgsMap[rec.deneme].sum += rec.subjects.toplam.n;
                    examAvgsMap[rec.deneme].count++;
                }
            });

            const labels = records.map(r => r.deneme);
            const studentNets = records.map(r => r.subjects && r.subjects.toplam ? r.subjects.toplam.n : 0);
            
            // Map student's exams to the calculated school averages
            const schoolNets = records.map(r => {
                const stats = examAvgsMap[r.deneme];
                return stats ? parseFloat((stats.sum / stats.count).toFixed(2)) : 0;
            });

            progressChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Öğrenci Net Toplamı',
                            data: studentNets,
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59,130,246,0.1)',
                            borderWidth: 3,
                            pointBackgroundColor: '#3b82f6',
                            pointRadius: 5,
                            pointHoverRadius: 7,
                            tension: 0.3,
                            fill: true
                        },
                        {
                            label: 'Okul Genel Net Ortalaması',
                            data: schoolNets,
                            borderColor: '#ef4444',
                            backgroundColor: 'transparent',
                            borderWidth: 2.5,
                            borderDash: [5, 5],
                            pointBackgroundColor: '#ef4444',
                            pointRadius: 4,
                            tension: 0.3,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false // We use our custom legend in HTML
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            padding: 12,
                            backgroundColor: isDark ? '#1e293b' : '#ffffff',
                            titleColor: isDark ? '#f8fafc' : '#0f172a',
                            bodyColor: isDark ? '#94a3b8' : '#475569',
                            borderColor: isDark ? '#334155' : '#e2e8f0',
                            borderWidth: 1,
                            titleFont: { family: 'Plus Jakarta Sans', weight: '700' },
                            bodyFont: { family: 'Plus Jakarta Sans' }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 10 } }
                        },
                        y: {
                            min: 0,
                            max: 120,
                            grid: { color: gridColor },
                            ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 10 } }
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

        async function saveRecordsToDB(newRecords, message = "Veritabanı güncellendi") {
            if (!supabaseClient) {
                showToast("Bulut bağlantısı yok! Kayıt eklenemedi.", "error");
                return;
            }

            const examName = newRecords[0]?.deneme || "Bilinmeyen Sınav";

            try {
                // 1. Sınavlar tablosuna eklemeyi deneyelim
                const { error: errExam } = await supabaseClient
                    .from('exams')
                    .upsert({ name: examName }, { onConflict: 'name' });
                
                // 2. Şimdi bu sınava ait eski kayıtlar varsa onları silelim (tekrar yükleme desteği için)
                await supabaseClient
                    .from('exam_results')
                    .delete()
                    .eq('exam_name', examName);

                // 3. Öğrencileri toplu olarak exam_results tablosuna ekleyelim
                const recordsToInsert = newRecords.map(r => ({
                    exam_name: examName,
                    student_no: parseInt(r.no, 10) || null,
                    student_name: r.name,
                    student_class: r.class,
                    student_branch: r.branch,
                    subjects: r.subjects,
                    puan: parseFloat(r.puan) || 0,
                    siralama: parseInt(r.siralama, 10) || 0
                }));

                // 100'erli paketler halinde toplu ekleme yapalım
                const chunkSize = 100;
                for (let i = 0; i < recordsToInsert.length; i += chunkSize) {
                    const chunk = recordsToInsert.slice(i, i + chunkSize);
                    const { error: errInsert } = await supabaseClient
                        .from('exam_results')
                        .insert(chunk);
                    
                    if (errInsert) {
                        console.error("Supabase bulk insert error:", errInsert);
                        showToast("Hata: Sınav verileri kaydedilirken sorun oluştu.", "error");
                        return;
                    }
                }

                showToast(message);
                await loadExamData();

            } catch (e) {
                console.error("saveRecordsToDB exception:", e);
                showToast("Bulut veritabanına bağlanırken hata oluştu.", "error");
            }
        }

        async function resetToDefault() {
            if (!supabaseClient) {
                showToast("Bulut bağlantısı yok! İşlem gerçekleştirilemedi.", "error");
                return;
            }

            if (!confirm("Tüm sınav verilerini veritabanından kalıcı olarak silmek ve sistemi sıfırlamak istediğinize emin misiniz?")) return;

            try {
                // Sınavlar tablosundaki tüm satırları silelim. Cascade silme sayesinde exam_results tablosundaki sonuçlar da otomatik silinecektir!
                const { error } = await supabaseClient
                    .from('exams')
                    .delete()
                    .neq('id', 0); // Hepsini silsin
                
                if (error) {
                    console.error("Supabase clear error:", error);
                    showToast("Veriler silinirken hata oluştu.", "error");
                } else {
                    showToast("Tüm sınav verileri buluttan kalıcı olarak silindi.");
                    activeStudent = null;
                    document.getElementById('student-report-card').style.display = 'none';
                    document.getElementById('welcome-panel-analysis').style.display = 'block';
                    document.getElementById('search-student').value = '';
                    await loadExamData();
                }
            } catch (e) {
                console.error("clear error exception:", e);
                showToast("Veritabanına bağlanırken hata oluştu.", "error");
            }
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
            if (document.getElementById('stat-students')) document.getElementById('stat-students').innerText = totalStudentsCount;
            if (document.getElementById('stat-exams')) document.getElementById('stat-exams').innerText = totalExamsCount;
            if (document.getElementById('stat-avg-net')) document.getElementById('stat-avg-net').innerText = schoolAvgNet;

            // Update Mobile Stats
            if (document.getElementById('stat-students-mobile')) document.getElementById('stat-students-mobile').innerText = totalStudentsCount;
            if (document.getElementById('stat-exams-mobile')) document.getElementById('stat-exams-mobile').innerText = totalExamsCount;
            if (document.getElementById('stat-avg-net-mobile')) document.getElementById('stat-avg-net-mobile').innerText = schoolAvgNet;
        }

        // Search logic
        function initSearch() {
            const searchInput = document.getElementById('search-student');
            const resultsList = document.getElementById('search-results-list');

            searchInput.addEventListener('input', () => {
                const query = searchInput.value.toLocaleLowerCase('tr-TR').trim();
                const clearBtn = document.getElementById('clear-search-student');
                if (clearBtn) {
                    clearBtn.style.display = query.length > 0 ? 'inline-flex' : 'none';
                }
                if (query.length < 1) {
                    resultsList.style.display = 'none';
                    return;
                }

                const matchingStudents = [];
                const addedIds = new Set();

                examDatabase.forEach(r => {
                    const matchesName = r.name.toLocaleLowerCase('tr-TR').includes(query);
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
            const match = examName.match(/(\d{2})[\/.-](\d{2})[\/.-](\d{4})/);
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

            renderProgressChart(records);
            
            // Switch to Karne tab on mobile
            if (window.innerWidth <= 768) {
                switchAnalysisTab('karne');
            }
        }

                async function printKarne() {
            // schoolData yüklenmemişse yükle
            await loadSchoolData();

            // 1. Grafik görüntüsünü al
            const chartCanvas = document.getElementById('progressChart');
            const chartImg = chartCanvas ? chartCanvas.toDataURL('image/png') : null;

            // 2. Sonuç tablosunu al
            const tableEl = document.getElementById('results-table');
            const tableHTML = tableEl ? tableEl.outerHTML : '<p>Tablo bulunamadı.</p>';

            // 3. Öğrenci bilgilerini al
            const studentName = document.getElementById('report-student-name')?.innerText || '-';
            const studentNo   = document.getElementById('report-student-no')?.innerText || '-';
            const studentClass = document.getElementById('report-student-class')?.innerText || '-';
            const studentBranch = document.getElementById('report-student-branch')?.innerText || '-';
            const examCount   = document.getElementById('report-student-exam-count')?.innerText || '-';

            // 4. Öğrenci numarasını ayıkla (örn. "No: 136" -> "136")
            const noMatch = studentNo.match(/\d+/);
            const noStr = noMatch ? noMatch[0] : '';

            // 5. Sicil kayıtlarını schoolData'dan çek
            let historyHTML = '<p style="color:#6b7280; font-size:8pt;">Bu öğrenciye ait belge geçmişi bulunmamaktadır.</p>';
            if (noStr && typeof schoolData !== 'undefined' && schoolData.ogrenci) {
                const ogr = schoolData.ogrenci.find(s => String(s.no) === noStr);
                if (ogr && ogr.history && ogr.history.length > 0) {
                    historyHTML = '<table style="width:100%; border-collapse:collapse; font-size:8pt;">';
                    historyHTML += '<thead><tr style="background:#f3f4f6;"><th style="padding:3px 6px; text-align:left; border:1px solid #d1d5db;">Belge Türü</th><th style="padding:3px 6px; text-align:left; border:1px solid #d1d5db;">Tarih</th><th style="padding:3px 6px; text-align:left; border:1px solid #d1d5db;">Detay</th></tr></thead><tbody>';
                    ogr.history.forEach(h => {
                        historyHTML += `<tr><td style="padding:3px 6px; border:1px solid #d1d5db;">${h.tur || '-'}</td><td style="padding:3px 6px; border:1px solid #d1d5db;">${h.tarih || '-'}</td><td style="padding:3px 6px; border:1px solid #d1d5db;">${h.detay || '-'}</td></tr>`;
                    });
                    historyHTML += '</tbody></table>';
                }
            }

            // 6. Karne HTML'ini oluştur
            const today = new Date();
            const dateStr = today.getDate().toString().padStart(2,'0') + '/' + (today.getMonth()+1).toString().padStart(2,'0') + '/' + today.getFullYear();

            const karneHTML = `
                <div style="font-family:'Inter',sans-serif; color:#111;">
                    <!-- Başlık -->
                    <div style="text-align:center; border-bottom:2px solid #111; padding-bottom:6px; margin-bottom:10px;">
                        <div style="font-size:10pt; font-weight:700; text-transform:uppercase; letter-spacing:1px;">CEYLANPINAR FEN LİSESİ</div>
                        <div style="font-size:16pt; font-weight:800; margin:2px 0;">ÖĞRENCİ DENEME ANALİZ KARNESİ</div>
                        <div style="font-size:8pt; color:#555;">Baskı Tarihi: ${dateStr}</div>
                    </div>

                    <!-- Öğrenci Bilgileri -->
                    <div style="display:flex; justify-content:space-between; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 12px; margin-bottom:12px; font-size:9pt;">
                        <div><strong>Ad Soyad:</strong> ${studentName}</div>
                        <div><strong>${studentNo}</strong></div>
                        <div><strong>${studentClass}</strong></div>
                        <div><strong>${studentBranch}</strong></div>
                        <div><strong>${examCount}</strong></div>
                    </div>

                    <!-- Deneme Sonuçları Tablosu -->
                    <div style="font-size:8pt; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px; color:#374151;">📊 Deneme Sınav Sonuçları</div>
                    <div style="width:100%; overflow:visible; margin-bottom:12px;">
                        ${tableHTML}
                    </div>

                    <!-- Net Gelişim Grafiği -->
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <div style="font-size:8pt; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; color:#374151;">📈 Net Gelişim Grafiği</div>
                        <div style="font-size:7.5pt; color:#4b5563; font-weight:600;">Mavi: Öğrenci | Kırmızı: Okul Ortalaması</div>
                    </div>
                    ${chartImg ? `<img src="${chartImg}" style="width:100%; max-height:160px; object-fit:contain; object-position:left; border:1px solid #e2e8f0; border-radius:4px; margin-bottom:14px;" />` : '<p style="color:#6b7280; font-size:8pt; margin-bottom:14px;">Grafik bulunamadı.</p>'}

                    <!-- Sicil Kaydı -->
                    <div style="font-size:8pt; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px; color:#374151;">📋 Öğrenci İşlem Geçmişi (Sicil)</div>
                    ${historyHTML}
                </div>
            `;

            const printArea = document.getElementById('karne-print-area');
            printArea.innerHTML = karneHTML;
            printArea.style.display = 'block';
            document.body.classList.add('print-karne');

            const originalTitle = document.title;
            const fileDateStr = dateStr.replace(/\//g, '.');
            document.title = `Öğrenci Analizi - ${studentName.trim()} - ${fileDateStr}`;

            setTimeout(() => {
                window.print();
                setTimeout(() => {
                    document.body.classList.remove('print-karne');
                    printArea.style.display = 'none';
                    printArea.innerHTML = '';
                    document.title = originalTitle;
                }, 500);
            }, 300);
        }

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
    
    final_html = html_template.replace("/* DATABASE_PLACEHOLDER */", records_js_str)
    final_html = final_html.replace("/* OKUL_DATABASE_PLACEHOLDER */", okul_js_str)
    final_html = final_html.replace("<!-- LEFT_NEWS_PLACEHOLDER -->", left_news_html)
    final_html = final_html.replace("<!-- RIGHT_NEWS_PLACEHOLDER -->", right_news_html)
    
    with open(html_out_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Merged web application HTML successfully compiled at: {html_out_path}")

if __name__ == "__main__":
    build_merged_app()
