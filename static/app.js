function fecharMenu(menu) {
    const card = menu.closest(".task-card");
    card?.classList.add("menu-closing");

    menu.classList.remove("show");
    menu.previousElementSibling?.setAttribute("aria-expanded", "false");

    setTimeout(() => card?.classList.remove("menu-closing"), 190);
}

function fecharMenus(exceto = null) {
    document.querySelectorAll(".priority-menu.show, .status-menu.show")
        .forEach((menu) => {
            if (menu !== exceto) fecharMenu(menu);
        });
}

document.addEventListener("click", (event) => {
    const botao = event.target.closest(".priority-button, .status-button");

    if (!botao) {
        fecharMenus();
        return;
    }

    const menu = botao.nextElementSibling;
    const vaiAbrir = !menu.classList.contains("show");

    fecharMenus(menu);
    if (vaiAbrir) {
        menu.classList.add("show");
        botao.setAttribute("aria-expanded", "true");
    } else {
        fecharMenu(menu);
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        const menuAberto = document.querySelector(".priority-menu.show, .status-menu.show");
        fecharMenus();
        menuAberto?.previousElementSibling?.focus();
    }
});

document.querySelectorAll(".task-toggle-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
        // No segundo envio, deixa o formulário seguir o fluxo que já existe.
        if (form.dataset.animacaoPronta === "1") {
            delete form.dataset.animacaoPronta;
            return;
        }

        event.preventDefault();
        event.stopPropagation();

        // Evita dois envios enquanto a animação acontece.
        if (form.dataset.animando === "1") return;
        form.dataset.animando = "1";

        const card = form.closest(".task-card");
        const reabrindo = card.classList.contains("is-completed");
        card.classList.add(reabrindo ? "is-unchecking" : "is-checking");

        const botao = event.submitter || form.querySelector('button[type="submit"]');
        const reduzirMovimento = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        setTimeout(() => {
            form.dataset.animacaoPronta = "1";
            delete form.dataset.animando;
            form.requestSubmit(botao);
        }, reduzirMovimento ? 0 : 280);
    });
});

document.addEventListener("submit", async (event) => {
    const form = event.target;
    const pagina = new URL(window.location.href);

    if (!form.closest(".task-card") || pagina.pathname !== "/") {
        return;
    }

    event.preventDefault();

    const card = form.closest(".task-card");
    const apagando = new URL(form.action).pathname.startsWith("/delete/");

    if (apagando && form.dataset.enviando === "1") return;

    if (apagando) {
        form.dataset.enviando = "1";
        card.classList.add("is-deleting");

        if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            await new Promise((resolver) => setTimeout(resolver, 220));
        }
    }

    const dados = new FormData(form);
    if (event.submitter?.name) {
        dados.append(event.submitter.name, event.submitter.value);
    }

    try {
        const resposta = await fetch(form.action, {
            method: "POST",
            body: dados,
            credentials: "same-origin",
            redirect: "manual"
        });

        if (resposta.type !== "opaqueredirect") {
            throw new Error("A atualização não foi confirmada.");
        }

        window.location.reload();
    } catch (erro) {
        if (apagando) {
            card.classList.remove("is-deleting");
            delete form.dataset.enviando;
        }
        alert("Não foi possível atualizar a tarefa. Tente novamente.");
    }
});

document.querySelectorAll(".flash li").forEach((aviso) => {
    setTimeout(() => {
        aviso.classList.add("saindo");
        setTimeout(() => aviso.remove(), 200);
    }, 3500);
});

const concluidas = document.querySelector(".completed-group");
const tituloConcluidas = concluidas?.querySelector("summary");

tituloConcluidas?.addEventListener("click", (event) => {
    if (!concluidas.open) return; // Ao abrir, mantém o comportamento normal.
    event.preventDefault();
    if (concluidas.dataset.fechando) return;

    concluidas.dataset.fechando = "1";

    const alturaRemovida = concluidas.getBoundingClientRect().height
        - tituloConcluidas.getBoundingClientRect().height;
    const limiteDepoisDeFechar = Math.max(
        0,
        document.documentElement.scrollHeight - alturaRemovida - window.innerHeight - 24
    );
    const posicaoTitulo = tituloConcluidas.getBoundingClientRect().top
        + window.scrollY - 16;
    const destino = Math.max(0, Math.min(posicaoTitulo, limiteDepoisDeFechar));

    const fechar = () => {
        concluidas.open = false;
        delete concluidas.dataset.fechando;
    };

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
        Math.abs(window.scrollY - destino) < 2) {
        window.scrollTo(0, destino);
        fechar();
    } else if ("onscrollend" in document) {
        document.addEventListener("scrollend", fechar, { once: true });
        window.scrollTo({ top: destino, behavior: "smooth" });
    } else {
        window.scrollTo({ top: destino, behavior: "smooth" });
        setTimeout(fechar, 900);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const anel = document.querySelector(".progress-ring");
    if (!anel) return;

    const chave = "progresso-anterior";

    document.addEventListener("submit", (event) => {
        const formulario = event.target;
        if (!(formulario instanceof HTMLFormElement)) return;

        if (/\/(?:toggle|status|delete)\//.test(formulario.action)) {
            sessionStorage.setItem(
                chave,
                anel.getAttribute("aria-valuenow")
            );
        }
    }, true);

    const anteriorSalvo = sessionStorage.getItem(chave);
    sessionStorage.removeItem(chave);

    if (anteriorSalvo === null ||
        window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        return;
    }

    const anterior = Number(anteriorSalvo);
    const atual = Number(anel.getAttribute("aria-valuenow"));

    if (!Number.isFinite(anterior) ||
        !Number.isFinite(atual) ||
        anterior === atual) {
        return;
    }

    const numero = anel.querySelector("span");
    anel.style.setProperty("--progress", anterior);
    if (numero) numero.textContent = `${Math.round(anterior)}%`;

    const inicio = performance.now();
    const duracao = 550;

    function animar(agora) {
        const tempo = Math.min((agora - inicio) / duracao, 1);
        const suavizado = 1 - Math.pow(1 - tempo, 3);
        const valor = anterior + (atual - anterior) * suavizado;

        anel.style.setProperty("--progress", valor);
        if (numero) numero.textContent = `${Math.round(valor)}%`;

        if (tempo < 1) requestAnimationFrame(animar);
    }

    requestAnimationFrame(animar);
});