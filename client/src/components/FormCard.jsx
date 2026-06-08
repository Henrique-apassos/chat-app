/**
 * FormCard — componente reutilizável para os formulários de autenticação.
 * Encapsula o layout do card branco centralizado, evitando duplicação
 * entre as telas de Login e Cadastro (princípio DRY).
 */
export default function FormCard({ titulo, children }) {
  return (
    <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-xl">
      <h2 className="text-center text-2xl font-bold text-[#06065D] mb-6">
        {titulo}
      </h2>
      {children}
    </div>
  )
}