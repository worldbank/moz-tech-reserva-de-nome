# 🇲🇿 Reserva de Nome 

## Requisitos

* [Python](https://python.org) 3.8.6
* [Poetry](https://python-poetry.org)

## Instalação

1. Instale as dependências do projeto:
    ```console
    $ poetry install
    ```
1. Crie as variáveis de ambiente:
    ```console
    $ poetry run createnv
    ```
1. Execute as migrações:
    ```console
    $ poetry run python manage.py migrate
    ```
1. Carregue as nacionalidades no banco de dados:
    ```console
    $ poetry run python manage.py loaddata nationalities.json
    ```
1. Colete os arquivos estáticos:
    ```console
    $ poetry run python manage.py collectstatic
    ```

## API Web

### `POST /api/name_application/available/`

#### Requisção

| Campo  | Tipo  | Descrição                                      |
| ------ | ----- | ---------------------------------------------- |
| `name` | `str` | Nome de empresa para consultar disponibilidade |

#### Resposta

| Campo       | Tipo   | Descrição                   |
| ----------- | ------ | --------------------------- |
| `name`      | `str`  | Nome de empresa consultado. |
| `available` | `bool` | Disponibilidade.            |

## Desenvolvimento

Para executar os testes:
```console
$ poetry run pytest
```

Para visualizar a aplicação:

```console
$ poetry run python manage.py runserver
```
E acesse o site em [`localhost:8000`](http://localhost:8000).