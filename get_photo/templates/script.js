import React from 'react';

function QrDownload(props) {
    const handleImageDownload = async () => {
        const myImage = sessionStorage.getItem('uploadedCloudPhotoUrl');
        if (myImage) {
            try {
                const response = await fetch(myImage);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const blob = await response.blob();
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = 'downloaded_image.png'; // 다운로드될 파일 이름 설정
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (error) {
                console.error('Error downloading the image:', error);
            }
        } else {
            alert('No image found in session storage.');
        }
    };

    const handleGifDownload = async () => {
        const myGif = sessionStorage.getItem('gifPhoto');
        if (myGif) {
            try {
                console.log('GIF URL:', myGif); // URL 확인
                const response = await fetch(myGif);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log('Response headers:', response.headers.get('Content-Type')); // 응답 헤더 확인
                const blob = await response.blob();
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = 'downloaded_image.gif'; // 다운로드될 파일 이름 설정
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (error) {
                console.error('Error downloading the GIF:', error);
            }
        } else {
            alert('No GIF found in session storage.');
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <button style={{ marginBottom: '20px' }} onClick={handleImageDownload}>
                Image Download
            </button>
            <button onClick={handleGifDownload}>
                Video Download
            </button>
        </div>
    );
}

export default QrDownload;

