import * as pdfjsLib from 'pdfjs-dist';

// Set worker source to the local file we copied
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

export const extractTextFromPDF = async (file) => {
    try {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let fullText = '';

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map((item) => item.str).join(' ');
            fullText += pageText + '\n\n';
        }

        return fullText.trim();
    } catch (error) {
        console.error('Error parsing PDF:', error);
        throw new Error('Failed to extract text from PDF');
    }
};
