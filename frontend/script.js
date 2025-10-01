// --- CONFIGURAÇÃO ---
const API_URL = 'http://127.0.0.1:8000';

// --- VARIÁVEL GLOBAL PARA GUARDAR O ACERVO COMPLETO ---
let acervoCompleto = [];

// --- SELETORES DE ELEMENTOS DO HTML ---
const plantasGrid = document.getElementById('plantas-grid');
const form = document.getElementById('planta-form');
const nomePopularInput = document.getElementById('nome_popular');
const nomeCientificoInput = document.getElementById('nome_cientifico');
const familiaInput = document.getElementById('familia');
const origemInput = document.getElementById('origem');
const cuidadosInput = document.getElementById('cuidados');
const clearBtn = document.getElementById('clear-btn');
const searchInput = document.getElementById('search-input');

// NOVOS SELETORES PARA EDIÇÃO
const plantaIdInput = document.getElementById('planta_id');
const submitBtn = document.getElementById('submit-btn');


// --- FUNÇÕES AUXILIARES DE FORMULÁRIO ---

// Limpa o formulário e reseta para o modo "Adicionar"
const clearForm = () => {
    form.reset();
    plantaIdInput.value = ''; // Limpa o ID oculto
    submitBtn.textContent = 'Adicionar à Enciclopédia'; // Reseta o texto do botão
};

// Carrega os dados da planta selecionada para o formulário
const loadFormForEdit = (planta) => {
    plantaIdInput.value = planta.id;
    nomePopularInput.value = planta.nome_popular;
    nomeCientificoInput.value = planta.nome_cientifico;
    familiaInput.value = planta.familia;
    origemInput.value = planta.origem;
    cuidadosInput.value = planta.cuidados;
    
    submitBtn.textContent = 'Salvar Alterações'; // Muda o texto do botão para indicar edição
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Rola para o formulário
};


// --- FUNÇÕES DA API (CRUD) ---

// LER todo o acervo da API
const fetchPlantas = async () => {
    try {
        const response = await fetch(`${API_URL}/plantas/`);
        if (!response.ok) throw new Error('Erro ao buscar plantas');
        acervoCompleto = await response.json();
        displayPlantas(acervoCompleto);
    } catch (error) {
        console.error('Falha ao buscar plantas:', error);
        plantasGrid.innerHTML = '<p style="color: red;">Não foi possível carregar o acervo. A API está rodando?</p>';
    }
};

// INCLUIR (POST) ou ALTERAR (PUT)
const handleFormSubmit = async (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return;
    }

    const plantaId = plantaIdInput.value;
    const method = plantaId ? 'PUT' : 'POST';
    const url = plantaId ? `${API_URL}/plantas/${plantaId}` : `${API_URL}/plantas/`;

    const plantaData = {
        nome_popular: nomePopularInput.value,
        nome_cientifico: nomeCientificoInput.value,
        familia: familiaInput.value,
        origem: origemInput.value,
        cuidados: cuidadosInput.value,
    };

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plantaData)
        });

        // Tratamento de erros, incluindo Bad Request (400) ou Not Found (404) do backend
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Erro ${response.status}: Falha na operação.`);
        }

        const action = plantaId ? 'atualizada' : 'adicionada';
        alert(`Planta ${action} com sucesso!`);
        
        clearForm();
        await fetchPlantas(); // Recarrega a lista

    } catch (error) {
        console.error(`Falha ao ${method === 'POST' ? 'adicionar' : 'alterar'}:`, error);
        alert(`ERRO: ${error.message}`);
    }
};

// DELETAR uma planta
const deletePlanta = async (id) => {
    if (!confirm(`Tem certeza que deseja EXCLUIR a planta com ID ${id}? Esta ação é irreversível.`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/plantas/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            // Se o backend retornou 404 (Not Found) ou 400
            const errorData = await response.json();
            throw new Error(errorData.detail || `Erro ${response.status}: Não foi possível deletar a planta.`);
        }

        await fetchPlantas(); 
        alert('Planta excluída com sucesso!');

    } catch (error) {
        console.error('Falha ao deletar:', error);
        alert(`ERRO: ${error.message}`);
    }
};


// --- FUNÇÕES DA INTERFACE ---

// Mostra as plantas na tela
const displayPlantas = (plantas) => {
    plantasGrid.innerHTML = '';
    plantas.forEach(planta => {
        const card = document.createElement('div');
        card.className = 'planta-card';
        
        card.innerHTML = `
            <div class="card-content">
                <h3>${planta.nome_popular}</h3>
                <p><em>${planta.nome_cientifico}</em></p>
                <p><strong>Família:</strong> ${planta.familia}</p>
                <p><strong>Origem:</strong> ${planta.origem}</p>
                <div class="cuidados"><strong>Cuidados:</strong> ${planta.cuidados}</div>
            </div>
            <div class="card-actions">
                <button class="btn-edit">Editar</button>
                <button class="btn-delete">Excluir</button>
            </div>
        `;
        
        // Adiciona os eventos aos botões
        card.querySelector('.btn-delete').addEventListener('click', () => deletePlanta(planta.id));
        
        // Usa a planta inteira para carregar o formulário de edição
        card.querySelector('.btn-edit').addEventListener('click', () => loadFormForEdit(planta)); 
        
        plantasGrid.appendChild(card);
    });
};

const handleSearch = (event) => {
    const searchTerm = event.target.value.toLowerCase();
    const plantasFiltradas = acervoCompleto.filter(planta => 
        planta.nome_popular.toLowerCase().includes(searchTerm) || 
        planta.nome_cientifico.toLowerCase().includes(searchTerm) ||
        planta.familia.toLowerCase().includes(searchTerm)
    );
    displayPlantas(plantasFiltradas);
};

// --- EVENT LISTENERS ---
document.addEventListener('DOMContentLoaded', fetchPlantas);
form.addEventListener('submit', handleFormSubmit); // Chama a função UNIFICADA (POST/PUT)
clearBtn.addEventListener('click', clearForm);
searchInput.addEventListener('input', handleSearch);