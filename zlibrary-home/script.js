const sections = ['business', 'psychology', 'selfhelp', 'society'];

sections.forEach(section => {
  fetch(`data/${section}.json`)
    .then(res => res.json())
    .then(books => {
      const container = document.querySelector(`#${section} .books`);
      books.forEach(book => {
        const div = document.createElement('div');
        div.className = 'book';
        div.innerHTML = `
          <img src="${book.cover}" alt="Copertina" class="cover" />
          <h3>${book.title}</h3>
          <p><strong>Autore:</strong> ${book.author}</p>
          <p><strong>Categoria:</strong> ${book.category}</p>
          <p><strong>Data:</strong> ${book.date}</p>
          <a href="${book.link}" target="_blank" class="download-btn">Scarica da Z-Library</a>
        `;
        container.appendChild(div);
      });
    });
});
