// CONFIGURAÇÃO
const API_URL = 'http://127.0.0.1:8000'; // URL base da API
let acervo = []; // Array para armazenar todas as plantas buscadas

// SELETORES DE ELEMENTOS
const grid = document.getElementById('plantas-grid');
const form = document.getElementById('planta-form');
const searchInput = document.getElementById('search-input');
const idInput = document.getElementById('planta_id'); // Campo oculto que guarda o ID para edição
const submitBtn = document.getElementById('submit-btn');

// Mapeamento dos inputs do formulário para facilitar a coleta de dados
const inputs = {
    nome_popular: document.getElementById('nome_popular'),
    nome_cientifico: document.getElementById('nome_cientifico'),
    familia: document.getElementById('familia'),
    origem: document.getElementById('origem'),
    cuidados: document.getElementById('cuidados')
};

// --- FUNÇÕES UTILS ---

// Limpa o formulário e o reseta para o modo "Adicionar"
const clearForm = () => {
    form.reset();
    idInput.value = ''; // Limpa o ID oculto
    submitBtn.textContent = 'Adicionar'; // Volta o texto do botão
};

// Carrega os dados de uma planta selecionada no formulário para edição (PUT)
const loadForm = (planta) => {
    idInput.value = planta.id;
    // Preenche todos os campos do formulário usando o mapeamento
    for (const key in inputs) {
        inputs[key].value = planta[key];
    }
    submitBtn.textContent = 'Salvar Alterações'; // Sinaliza o modo edição
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Rola para o formulário
};

// --- FUNÇÕES DA API (CRUD) ---

// (READ) Busca todas as plantas na API e as exibe
const fetchPlantas = async () => {
    try {
        const res = await fetch(`${API_URL}/plantas/`);
        acervo = await res.json();
        displayPlantas(acervo);
    } catch (e) {
        grid.innerHTML = `<p style="color: red;">API Offline. Verifique se o backend está rodando.</p>`;
    }
};

// (CREATE/UPDATE) Manipula o envio do formulário, decidindo se é POST ou PUT
const handleFormSubmit = async (e) => {
    e.preventDefault();
    const id = idInput.value;
    // Decide o método e URL: Se tem ID, é PUT (EDIÇÃO); senão, é POST (CRIAÇÃO)
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/plantas/${id}` : `${API_URL}/plantas/`;

    // Constrói o objeto de dados a ser enviado para a API
    const data = {};
    for (const key in inputs) {
        data[key] = inputs[key].value;
    }

    try {
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data) // Envia dados JSON
        });

        if (!res.ok) {
            // Trata erros de validação (400) ou outros erros do backend
            const errorData = await res.json();
            throw new Error(errorData.detail || `Erro ${res.status} na API.`);
        }

        alert(`Planta ${id ? 'atualizada' : 'adicionada'} com sucesso!`);
        clearForm();
        fetchPlantas(); // Recarrega a lista após o sucesso
    } catch (error) {
        alert(`FALHA: ${error.message}`);
    }
};

// (DELETE) Exclui uma planta
const deletePlanta = async (id) => {
    if (!confirm(`Tem certeza que deseja EXCLUIR a planta (ID: ${id})?`)) return;

    try {
        const res = await fetch(`${API_URL}/plantas/${id}`, { method: 'DELETE' });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || `Erro ${res.status} ao deletar.`);
        }

        alert('Planta excluída!');
        fetchPlantas(); // Recarrega a lista
    } catch (error) {
        alert(`FALHA: ${error.message}`);
    }
};

// --- UI / RENDER ---

// Renderiza os cards das plantas na interface
const displayPlantas = (plantas) => {
    grid.innerHTML = ''; // Limpa o grid
    plantas.forEach(p => {
        const card = document.createElement('div');
        card.className = 'planta-card';
        card.innerHTML = `
            <div class="card-content">
                <h3>${p.nome_popular}</h3>
                <p><em>${p.nome_cientifico}</em></p>
                <p><strong>Família:</strong> ${p.familia}</p>
                <p><strong>Cuidados:</strong> ${p.cuidados}</p>
            </div>
            <div class="card-actions">
                <button class="btn-edit">Editar</button>
                <button class="btn-delete">Excluir</button>
            </div>
        `;
        
        // Atribui as funções de CRUD aos botões
        card.querySelector('.btn-edit').addEventListener('click', () => loadForm(p));
        card.querySelector('.btn-delete').addEventListener('click', () => deletePlanta(p.id));
        grid.appendChild(card);
    });
};

// Filtra plantas com base no input de busca
const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = acervo.filter(p => 
        p.nome_popular.toLowerCase().includes(term) || 
        p.nome_cientifico.toLowerCase().includes(term)
    );
    displayPlantas(filtered);
};

// --- EVENT LISTENERS ---

// Carrega as plantas quando a página for totalmente carregada
document.addEventListener('DOMContentLoaded', fetchPlantas);

// Envia o formulário (POST/PUT)
form.addEventListener('submit', handleFormSubmit);

// Limpa o formulário
document.getElementById('clear-btn').addEventListener('click', clearForm);

// Executa a busca em tempo real
searchInput.addEventListener('input', handleSearch);