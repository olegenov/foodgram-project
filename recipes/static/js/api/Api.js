function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
    }
  getPurchases () {
    return fetch(`/api/v1/purchases/`, {
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(`/api/v1/purchases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        'recipe': id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removePurchases (id){
    return fetch(`/api/v1/purchases/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch('/api/v1/subscribe/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        'author': id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(`/api/v1/subscribe/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(`/api/v1/favorite/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        'recipe': id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(`/api/v1/favorite/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken")
      }
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(`/api/v1/ingredients/?query=${text}`, {
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
