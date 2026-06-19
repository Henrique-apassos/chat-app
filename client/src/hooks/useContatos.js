import { useState, useEffect } from "react";
import { API_URL } from "../services/api";

export function useContatos() {
    const [contatos, setContatos] = useState([]);
    // Efeito para buscar a lista de contatos do backend
    useEffect(() => {
        const buscarContatos = async () => {
            try {
                const resposta = await fetch(`${API_URL}/auth/usuarios`);

                if (resposta.ok) {
                    const dados = await resposta.json();
                    setContatos(dados);
                } else {
                    throw new Error("Rota não encontrada ou erro no servidor");
                }
            } catch (error) {
                console.error("Erro ao carregar os contatos reais:", error);
                setContatos([
                    { usuario: 'maria', nome: 'Maria Silva' },
                    { usuario: 'joao', nome: 'João Pedro' },
                    { usuario: 'carlos', nome: 'Carlos Tech' }
                ]);
            }
        };

        buscarContatos();
    }, []);

    return contatos;
}