const headerText = document.getElementById('header-text').textContent;
document.getElementById('header').innerHTML = `
    <header>
        <b>${headerText}</b>
    </header>
`;