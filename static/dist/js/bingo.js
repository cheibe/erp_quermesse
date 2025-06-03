import fetchComTimeout from './tools.js';

class TabelaBingo {
    _numeros_sorteados = [];
    mudarCorAPI(number){
        if (this._numeros_sorteados.includes(number)){
            sortBingo()
            console.log(`tinha um numero, sorteado novamente ${this._numeros_sorteados}`)
        }
        this._numeros_sorteados.push(number)
        let numeroSorteado = document.getElementById(`cell-${number}`)
        numeroSorteado.classList.add('bg-danger', 'text-white')
        console.log(`fez um sorteio ${this._numeros_sorteados}`)

        if (number >= 1 && number <= 15){
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `B-${number}`
        }
        else if (number >= 16 && number <= 30) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `I-${number}`
        }
        else if (number >= 31 && number <= 45) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `N-${number}`
        }
        else if (number >= 46 && number <= 60) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `G-${number}`
        }
        else if (number >= 61 && number <= 75) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `O-${number}`
        }
    }

    cleanBingo(){
        this._numeros_sorteados = []
        console.log(this._numeros_sorteados)
        document.querySelectorAll('td').forEach(td => {
            td.classList.remove('bg-danger', 'text-white');
        });
        const circulo = document.getElementById('circulo')
        circulo.classList.add('d-none')
    }

    _getRandomIntInclusive(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    mudarCorJS(){
        let number = this._getRandomIntInclusive(1,75)
        if (this._numeros_sorteados.includes(number)){
            let number = this._getRandomIntInclusive(1,75)
            return number
        }
        this._numeros_sorteados.push(number)
        let numeroSorteado = document.getElementById(`cell-${number}`)
        numeroSorteado.classList.add('bg-danger', 'text-white')
        if (number >= 1 && number <= 15){
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `B-${number}`
        }
        else if (number >= 16 && number <= 30) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `I-${number}`
        }
        else if (number >= 31 && number <= 45) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `N-${number}`
        }
        else if (number >= 46 && number <= 60) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `G-${number}`
        }
        else if (number >= 61 && number <= 75) {
            const pedra_cantada = document.getElementById('pedra')
            pedra_cantada.textContent = `O-${number}`
        }
    }
};

const tabelaBingo = new TabelaBingo()
function sortBingo() {
    const spinner = document.getElementById('loading-spinner');
    spinner.classList.remove('d-none');
    const circulo = document.getElementById('circulo')
    circulo.classList.add('d-none')
    var data = {
        'jsonrpc': '2.0',
        'method': 'generateIntegers',
        'params': {
            'apiKey': window.paramsJS,
            'n': 1,
            'min': 1,
            'max': 75,
        },
        'id': 10
    };
    fetchComTimeout('https://api.random.org/json-rpc/4/invoke', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    }, 8000)
    .then(response => {
        if (response.result.random.data[0] != []){
            const num = response.result.random.data[0];
            tabelaBingo.mudarCorAPI(num);
            circulo.classList.remove('d-none')
            circulo.classList.add('circulo-pedra-api')
        }
    })
    .catch(err => {
        if (err.name === 'AbortError') {
            console.log('O servidor demorou demais para responder (timeout).');
            tabelaBingo.mudarCorJS()
            circulo.classList.remove('d-none')
            circulo.classList.add('circulo-pedra-js')
        } else {
            console.error(err);
            console.log(`Ocorreu um erro: ${err.message}`);
            tabelaBingo.mudarCorJS()
            circulo.classList.remove('d-none')
            circulo.classList.add('circulo-pedra-js')
        }
    })
    .finally(() => {
        spinner.classList.add('d-none');
    })
}
document.getElementById('sort-btn')
        .addEventListener('click', sortBingo);

document.getElementById('clean-btn')
        .addEventListener('click', () => tabelaBingo.cleanBingo());

const tbody = document.getElementById('bingo-body');
for (let row = 0; row < 15; row++) {
    const tr = document.createElement('tr');
    for (let col = 0; col < 5; col++) {
        const num = col * 15 + row + 1;
        const td = document.createElement('td');
        td.id = `cell-${num}`;
        td.textContent = num;
        tr.appendChild(td);
    }
    tbody.appendChild(tr);
}

const btnFS = document.getElementById('fs-btn');
btnFS.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen?.()
            || document.documentElement.webkitRequestFullscreen?.()
            || document.documentElement.mozRequestFullScreen?.()
            || document.documentElement.msRequestFullscreen?.();
        btnFS.innerHTML = '<i class="bi bi-fullscreen-exit fs-4"></i>';
    } else {
        document.exitFullscreen?.()
            || document.webkitExitFullscreen?.()
            || document.mozCancelFullScreen?.()
            || document.msExitFullscreen?.();
        btnFS.innerHTML = '<i class="bi bi-arrows-fullscreen fs-4"></i>';
    }
});

document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement) {
        btnFS.innerHTML = '<i class="bi bi-arrows-fullscreen fs-4"></i>';
    }
});