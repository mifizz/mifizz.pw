const headerText = document.getElementById("header-text").textContent;
document.getElementById("header").innerHTML = `
  <a href="/">
  <img class="img-bordered img-head"
  src="/static/images/head.jpg"
  alt="Здесь могла быть ваша реклама"/>
  </a>
  <header>
      <b>${headerText}</b>
  </header>
`;
