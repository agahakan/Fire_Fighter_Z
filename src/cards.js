import { API_URL } from "./game";

export default class Card {
  constructor() {
    this.cards = [];
    this.json_obj = [];
  }

  initClickEvent(data) {
    this.cards.forEach((card) => {
      card.addEventListener("click", () => {
        const tab_id = card.getAttribute("tab_id");
        const card_id = card.getAttribute("card_id");
        const activeCard = data[tab_id];
        data.splice(tab_id, 1);
        card.classList.add("selected");
        setTimeout(() => {
          card.parentNode.removeChild(card);
          this.playDrawcard(card_id);
        }, 700);
      });
    });
  }

  async fetchCards() {
    let response = await fetch(`${API_URL}/init`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    let data = await response.json();
    localStorage.setItem("listCards", JSON.stringify(data));
    const listCards = localStorage.getItem("listCards");
    this.json_obj = JSON.parse(listCards);
    return this.json_obj;
  }

  createCards(data) {
    const cardsContainer = document.querySelector(".cards");
    cardsContainer.innerHTML = "";

    for (let i = 0; i < data.length; i++) {
      const cardsData = data[i];
      const cardElement = document.createElement("div");
      cardElement.setAttribute("tab_id", i);
      cardElement.setAttribute("card_id", cardsData.id);
      cardElement.classList.add("cards__item");
      cardElement.classList.add(`card-${i + 1}`);

      cardElement.innerHTML = `
      <img src="./Cards/${cardsData.Path}">
    `;
      cardsContainer.appendChild(cardElement);
    }
    this.cards = document.querySelectorAll(".cards__item");
    this.initClickEvent(data);
  }

  async getCards() {
    const data = await this.fetchCards();
    this.createCards(data);
  }

  async playDrawcard(id) {
    let response = await fetch(`${API_URL}/play_drawcard?id=` + id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    let data = await response.json();
    localStorage.setItem("listPlayerCards", JSON.stringify(data));
    const listCards = localStorage.getItem("listPlayerCards");
    this.json_obj = JSON.parse(listCards);
    this.createCards(this.json_obj);
  }
}