import pytest
from pytest_bdd import scenario, given, when, then, parsers

from app.models.mensagem import MensagemModel
from app.models.recebe import RecebeModel
from app.database import get_db
from main import app


# ==========================================
# MAPEAMENTO DOS CENÁRIOS
# ==========================================

@scenario('Edicao_Mensagens.feature', 'Edição de mensagem própria')
def test_edicao_mensagem_propria():
    pass


@scenario('Edicao_Mensagens.feature', 'Tentativa de editar mensagem de outro usuário')
def test_tentativa_editar_mensagem_de_outro_usuario():
    pass


@scenario('Exclusao_de_Mensagem.feature', 'Exclusão de mensagem própria')
def test_exclusao_mensagem_propria():
    pass


@scenario('Exclusao_de_Mensagem.feature', 'Tentativa de excluir mensagem de outro usuário')
def test_tentativa_excluir_mensagem_de_outro_usuario():
    pass


@scenario('Exclusao_de_Mensagem.feature', 'Atualização da conversa após exclusão de mensagem')
def test_atualizacao_conversa_apos_exclusao():
    pass


# ==========================================
# FIXTURE
# ==========================================

@pytest.fixture
def contexto(client):
    estado = {
        "db": next(app.dependency_overrides[get_db]()),
        "usuario_atual": None,
        "mensagem_id": None,
        "response": None,
        "texto_original": None
    }

    yield estado


# ==========================================
# FUNÇÃO AUXILIAR
# ==========================================

def criar_mensagem(db, remetente, destinatario, texto):
    mensagem = MensagemModel(
        timestamp="2026-06-08 20:00:00",
        texto=texto,
        status_envio="ENVIADO",
        usuario=remetente,
        id_grupo=None
    )

    db.add(mensagem)
    db.commit()
    db.refresh(mensagem)

    recebimento = RecebeModel(
        usuario=destinatario,
        id_mensagem=mensagem.id_mensagem,
        lida=0
    )

    db.add(recebimento)
    db.commit()

    return mensagem.id_mensagem


# ==========================================
# GIVEN
# ==========================================

@given(parsers.parse('que estou na conversa com "{usuario}"'))
@given(parsers.parse('estou na conversa com "{usuario}"'))
def estou_na_conversa(usuario, contexto):
    contexto["usuario_conversa"] = usuario
    contexto["usuario_atual"] = "eu"


@given("existe uma mensagem enviada por mim")
def existe_mensagem_enviada_por_mim(contexto):
    db = contexto["db"]
    contexto["texto_original"] = "Mensagem original"

    contexto["mensagem_id"] = criar_mensagem(
        db=db,
        remetente="eu",
        destinatario=contexto["usuario_conversa"],
        texto=contexto["texto_original"]
    )


@given(parsers.parse('existe uma mensagem enviada por "{usuario}"'))
def existe_mensagem_enviada_por_outro_usuario(usuario, contexto):
    db = contexto["db"]
    contexto["texto_original"] = "Mensagem original"

    contexto["mensagem_id"] = criar_mensagem(
        db=db,
        remetente=usuario,
        destinatario="eu",
        texto=contexto["texto_original"]
    )


@given("excluí uma mensagem")
def exclui_uma_mensagem(client, contexto):
    db = contexto["db"]

    id_mensagem = criar_mensagem(
        db=db,
        remetente="eu",
        destinatario=contexto["usuario_conversa"],
        texto="Mensagem excluída"
    )

    response = client.request(
        "DELETE",
        f"/mensagens/{id_mensagem}",
        json={"usuario": "eu"}
    )

    contexto["mensagem_id"] = id_mensagem
    contexto["response"] = response


@given("a exclusão foi autorizada")
def exclusao_foi_autorizada(contexto):
    assert contexto["response"].status_code == 200


# ==========================================
# WHEN
# ==========================================

@when(parsers.parse('edito a mensagem para "{novo_texto}"'))
def edito_mensagem(client, novo_texto, contexto):
    response = client.put(
        f"/mensagens/{contexto['mensagem_id']}",
        json={
            "usuario": contexto["usuario_atual"],
            "novo_texto": novo_texto
        }
    )

    contexto["response"] = response


@when("tento editar essa mensagem")
def tento_editar_mensagem(client, contexto):
    response = client.put(
        f"/mensagens/{contexto['mensagem_id']}",
        json={
            "usuario": contexto["usuario_atual"],
            "novo_texto": "Texto alterado indevidamente"
        }
    )

    contexto["response"] = response


@when("solicito a exclusão da mensagem")
def solicito_exclusao(client, contexto):
    response = client.request(
        "DELETE",
        f"/mensagens/{contexto['mensagem_id']}",
        json={"usuario": contexto["usuario_atual"]}
    )

    contexto["response"] = response


@when("tento excluir essa mensagem")
def tento_excluir_mensagem(client, contexto):
    response = client.request(
        "DELETE",
        f"/mensagens/{contexto['mensagem_id']}",
        json={"usuario": contexto["usuario_atual"]}
    )

    contexto["response"] = response


@when("a conversa é aberta")
def conversa_e_aberta(contexto):
    contexto["conversa_aberta"] = True


# ==========================================
# THEN
# ==========================================

@then("a mensagem deve ser atualizada na conversa")
def mensagem_deve_ser_atualizada(contexto):
    assert contexto["response"].status_code == 200

    db = contexto["db"]
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == contexto["mensagem_id"]
    ).first()

    assert mensagem.texto == "Mensagem Editada"


@then("deve aparecer como editada")
def deve_aparecer_como_editada(contexto):
    assert contexto["response"].json()["editada"] is True


@then("o sistema deve impedir a edição")
def sistema_deve_impedir_edicao(contexto):
    assert contexto["response"].status_code == 403


@then("a mensagem deve permanecer sem alteração")
def mensagem_deve_permanecer_sem_alteracao(contexto):
    db = contexto["db"]
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == contexto["mensagem_id"]
    ).first()

    assert mensagem.texto == contexto["texto_original"]


@then("a mensagem deve ser removida da conversa")
def mensagem_deve_ser_removida(contexto):
    assert contexto["response"].status_code == 200

    db = contexto["db"]
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == contexto["mensagem_id"]
    ).first()

    assert mensagem is None


@then("o sistema deve impedir a exclusão")
def sistema_deve_impedir_exclusao(contexto):
    assert contexto["response"].status_code == 403


@then("a mensagem deve permanecer na conversa")
def mensagem_deve_permanecer_na_conversa(contexto):
    db = contexto["db"]
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == contexto["mensagem_id"]
    ).first()

    assert mensagem is not None


@then("a mensagem não deve aparecer na conversa")
def mensagem_nao_deve_aparecer_na_conversa(contexto):
    db = contexto["db"]
    mensagem = db.query(MensagemModel).filter(
        MensagemModel.id_mensagem == contexto["mensagem_id"]
    ).first()

    assert mensagem is None