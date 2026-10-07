const https = require('https');
const fs = require('fs');
const path = require('path');

const FOLDER_ID = '13PQ00XpHrnTHsTmkUQ-SpeUr0RGOx8Tu';
const DEFAULT_FILE_ID = '1UrkuCd5EzoouDxapC_-z79cpGOnd_33_';

function fetchUrl(url, options = {}) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }, ...options }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return resolve(fetchUrl(res.headers.location, options));
      }
      resolve(res);
    }).on('error', reject);
  });
}

async function getLatestFileId() {
  try {
    const res = await fetchUrl(`https://drive.google.com/drive/folders/${FOLDER_ID}`);
    let data = '';
    for await (const chunk of res) {
      data += chunk;
    }
    const matches = data.match(/"(1[a-zA-Z0-9_-]{32,})"/g) || [];
    const uniqueIds = [...new Set(matches.map(m => m.replace(/"/g, '')))].filter(id => id !== FOLDER_ID);
    if (uniqueIds.length > 0) {
      return uniqueIds[0];
    }
  } catch (e) {
    console.error('Error finding file from folder:', e);
  }
  return DEFAULT_FILE_ID;
}

module.exports = async (req, res) => {
  try {
    const fileId = await getLatestFileId();
    const downloadUrl = `https://drive.usercontent.google.com/download?id=${fileId}&export=download&confirm=t`;
    
    const fileRes = await fetchUrl(downloadUrl);
    
    if (fileRes.statusCode === 200) {
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', 'attachment; filename="Jaykumar_Kadao_Resume.pdf"');
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
      return fileRes.pipe(res);
    }
  } catch (err) {
    console.error('Download error:', err);
  }

  // Fallback to local file if available
  try {
    const localPath = path.join(process.cwd(), 'assets', 'Jaykumar_Kadao_Resume.pdf');
    if (fs.existsSync(localPath)) {
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', 'attachment; filename="Jaykumar_Kadao_Resume.pdf"');
      return fs.createReadStream(localPath).pipe(res);
    }
  } catch (fallbackErr) {
    console.error('Fallback error:', fallbackErr);
  }

  res.status(500).send('Unable to download resume');
};
