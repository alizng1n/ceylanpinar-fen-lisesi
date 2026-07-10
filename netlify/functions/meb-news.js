// netlify/functions/meb-news.js
// MEB okul sitesinden haber ve duyuruları sunucu tarafında cekmek icin Netlify Function.
// Tarayici CORS kisitlamasini asarak dogrudan MEB sitesine baglanir.

const https = require('https');

exports.handler = async function(event, context) {
    const targetUrl = 'https://ceylanpinarfenlisesi.meb.k12.tr';

    try {
        const html = await fetchPage(targetUrl);
        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=1800' // 30 dakika cache
            },
            body: JSON.stringify({ contents: html })
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify({ error: error.message })
        };
    }
};

function fetchPage(url) {
    return new Promise((resolve, reject) => {
        const req = https.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'identity'
            },
            timeout: 8000
        }, (response) => {
            // Yonlendirme varsa takip et
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                fetchPage(response.headers.location).then(resolve).catch(reject);
                return;
            }

            if (response.statusCode !== 200) {
                reject(new Error(`HTTP ${response.statusCode}`));
                return;
            }

            const chunks = [];
            response.on('data', chunk => chunks.push(chunk));
            response.on('end', () => {
                const buffer = Buffer.concat(chunks);
                // UTF-8 dene, hata varsa latin1 kullan
                let html;
                try {
                    html = buffer.toString('utf8');
                } catch (e) {
                    html = buffer.toString('latin1');
                }
                resolve(html);
            });
            response.on('error', reject);
        });

        req.on('error', reject);
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Baglanti zaman asimina ugradi'));
        });
    });
}
