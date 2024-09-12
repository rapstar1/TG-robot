function createWallet() {
    fetch('http://127.0.0.1:5000/api/create-wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        console.log(data); // 添加日志以调试数据
        if (data.address && data.mnemonic) {
            document.getElementById('mainMenu').style.display = 'none';
            document.getElementById('walletInfo').style.display = 'block';
            document.getElementById('walletAddress').textContent = data.address;
            document.getElementById('walletMnemonic').textContent = data.mnemonic;
        } else {
            alert('创建钱包失败，请重试！');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('创建钱包失败，请检查网络连接！');
    });
}

function goBack() {
    document.getElementById('walletInfo').style.display = 'none';
    document.getElementById('mainMenu').style.display = 'block';
}