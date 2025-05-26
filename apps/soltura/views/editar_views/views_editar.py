from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models.models import Soltura
from rest_framework import status
from ...service_soltura.service_edit_soltura_by_id.edit_soltura_by_id_service import editar_soltura_por_id

@api_view(['PUT'])
def editar_soltura_view(request, soltura_id):
    try:
        soltura = editar_soltura_por_id(soltura_id, request.data)
        return Response({"mensagem": "soltura atualizada com sucesso."}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"erro": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        return Response({"erro": f"Campo obrigatório faltando: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"erro": "Erro interno ao atualizar soltura."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
