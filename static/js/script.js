// Dados dos produtos (em uma aplicação real, isso viria da API Flask)
let produtos = [
  { id: 1, nome: "Sabão", categoria: "Limpeza", preco: 5.99, estoque: 50 },
  { id: 2, nome: "Pão", categoria: "Alimentos", preco: 3.5, estoque: 20 },
  { id: 3, nome: "Tênis", categoria: "Calçados", preco: 129.9, estoque: 10 },
]

let produtoEditando = null

// Função para renderizar produtos
function renderizarProdutos(produtosParaRender = produtos) {
  const lista = document.getElementById("produtos-lista")

  if (produtosParaRender.length === 0) {
    lista.innerHTML = '<div class="empty-state">Nenhum produto encontrado.</div>'
    return
  }

  lista.innerHTML = produtosParaRender
    .map(
      (produto) => `
        <div class="produto-card">
            <div class="produto-header">
                <div class="produto-info">
                    <h3>
                        ${produto.nome}
                        <span class="categoria-badge categoria-${produto.categoria.toLowerCase()}">
                            ${produto.categoria}
                        </span>
                    </h3>
                    <div class="produto-detalhes">
                        <span><i class="fas fa-dollar-sign"></i> R$ ${produto.preco.toFixed(2)}</span>
                        <span><i class="fas fa-boxes"></i> ${produto.estoque} unidades</span>
                    </div>
                </div>
                <div class="produto-acoes">
                    <button class="btn-edit" onclick="editarProduto(${produto.id})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn-delete" onclick="confirmarDelecao(${produto.id})">
                        <i class="fas fa-trash"></i> Deletar
                    </button>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

// Função para filtrar produtos
function filtrarProdutos() {
  const busca = document.getElementById("busca").value.toLowerCase()
  const produtosFiltrados = produtos.filter((produto) => produto.nome.toLowerCase().includes(busca))
  renderizarProdutos(produtosFiltrados)
}

// Função para abrir modal
function abrirModal(produto = null) {
  const modal = document.getElementById("modal")
  const titulo = document.getElementById("modal-titulo")
  const form = document.getElementById("produto-form")

  if (produto) {
    titulo.textContent = "Editar Produto"
    document.getElementById("nome").value = produto.nome
    document.getElementById("categoria").value = produto.categoria
    document.getElementById("preco").value = produto.preco
    document.getElementById("estoque").value = produto.estoque
    produtoEditando = produto
  } else {
    titulo.textContent = "Adicionar Novo Produto"
    form.reset()
    produtoEditando = null
  }

  modal.style.display = "block"
}

// Função para fechar modal
function fecharModal() {
  document.getElementById("modal").style.display = "none"
  produtoEditando = null
}

// Função para editar produto
function editarProduto(id) {
  const produto = produtos.find((p) => p.id === id)
  abrirModal(produto)
}

// Função para confirmar deleção
function confirmarDelecao(id) {
  if (confirm("Tem certeza que deseja deletar este produto?")) {
    deletarProduto(id)
  }
}

// Função para deletar produto
function deletarProduto(id) {
  // Em uma aplicação real, você faria uma requisição DELETE para sua API Flask
  produtos = produtos.filter((p) => p.id !== id)
  renderizarProdutos()

  // Exemplo de como seria a requisição para Flask:
  /*
    fetch(`/api/produtos/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            produtos = produtos.filter(p => p.id !== id);
            renderizarProdutos();
        }
    });
    */
}

// Função para salvar produto
function salvarProduto(dadosProduto) {
  if (produtoEditando) {
    // Editar produto existente
    const index = produtos.findIndex((p) => p.id === produtoEditando.id)
    produtos[index] = { ...produtoEditando, ...dadosProduto }
  } else {
    // Adicionar novo produto
    const novoId = produtos.length > 0 ? Math.max(...produtos.map((p) => p.id)) + 1 : 1
    produtos.push({ id: novoId, ...dadosProduto })
  }

  renderizarProdutos()
  fecharModal()

  // Em uma aplicação real, você faria uma requisição POST/PUT para sua API Flask:
  /*
    const method = produtoEditando ? 'PUT' : 'POST';
    const url = produtoEditando ? `/api/produtos/${produtoEditando.id}` : '/api/produtos';
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dadosProduto)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recarregar produtos da API
            carregarProdutos();
        }
    });
    */
}

// Event listeners
document.getElementById("produto-form").addEventListener("submit", (e) => {
  e.preventDefault()

  const dadosProduto = {
    nome: document.getElementById("nome").value,
    categoria: document.getElementById("categoria").value,
    preco: Number.parseFloat(document.getElementById("preco").value),
    estoque: Number.parseInt(document.getElementById("estoque").value),
  }

  salvarProduto(dadosProduto)
})

// Fechar modal ao clicar fora dele
window.addEventListener("click", (e) => {
  const modal = document.getElementById("modal")
  if (e.target === modal) {
    fecharModal()
  }
})

// Carregar produtos ao inicializar a página
document.addEventListener("DOMContentLoaded", () => {
  renderizarProdutos()
})

// Função para carregar produtos da API Flask (exemplo)
function carregarProdutos() {
  /*
    fetch('/api/produtos')
        .then(response => response.json())
        .then(data => {
            produtos = data.produtos;
            renderizarProdutos();
        })
        .catch(error => {
            console.error('Erro ao carregar produtos:', error);
        });
    */
}
