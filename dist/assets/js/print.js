document.getElementById('print').addEventListener('click', () => {
    const content = document.querySelector('main').innerHTML;
    const head = document.querySelector('head').innerHTML;
    const foot = document.querySelector('foot').innerHTML;

    const newWindow = window.open('', '', 'width=800,height=600');
    newWindow.document.write(`
        <html>
        <head>${head}</head>
        <body>${content}</body>
        <foot>${foot}</foot>
        </html>
    `);
    newWindow.document.close();
    newWindow.print();
    newWindow.close();
});