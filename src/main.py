import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View
from flet.core.colors import Colors
from flet.core.dropdown import Option

def main(page: Page):
    page.title = "exemplo de rotas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667


    def gerenciar_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("home"), center_title=True, bgcolor=Colors.CYAN),
                    inss,
                    ElevatedButton(text="regras", on_click=lambda _: page.go("/regras")),
                    ElevatedButton(text="simulacao", on_click=lambda _: page.go("/simulacao")),

                ]
            )
        )

        if page.route == "/simulacao":
            page.views.append(
                View(
                    "/simulacao", [
                        AppBar(title=Text("simulação de aposentadoria"), center_title=True, bgcolor=Colors.CYAN),

                        meu_genero,
                        idade,
                        tempo_contribuicao,
                        media_salarial,
                        opcao,
                        ElevatedButton(text="Calcular", on_click=verificar_campos),
                        ElevatedButton(text="Regras", on_click=verificar_campos),
                        txt_alerta,


                    ]
                )
            )

        if page.route == "/regras":
            page.views.append(
                View(
                    "/regras", [
                        AppBar(title=Text("regras da aposentadoria"), center_title=True, bgcolor=Colors.CYAN),
                        ElevatedButton(text="regras", on_click=lambda _: page.go("/simulacao")),

                        ft.TextField('Regras Básicas de Aposentadoria:', text_size=18),
                        ft.Text('Aposentadoria por Idade:', size=16),
                        ft.Text('Homens: 65 anos de idade e pelo menos 15 anos de contribuição:', size=14),
                        ft.Text('Mulheres: 62 anos de idade e pelo menos 15 anos de contribuição:', size=14),

                        ft.TextField('Aposentadoria por Tempo de Contribuição:', text_size=18),
                        ft.Text('Homens: 35 anos de contribuição.', size=16),
                        ft.Text('Mulheres: 30 anos de contribuição.', size=14),

                        ft.TextField('Valor Estimado do Benefício:', text_size=18),

                        ft.Text(' O valor da aposentadoria será uma média de 60% da média salarial informada,'
                                ' acrescido de 2% por ano que exceder o tempo mínimo de contribuição.', size=16),

                    ]
                )
            )
        if page.route == "/resultados":
            calcular_beneficio()
            page.views.append(
                View(
                    '/resultados', [
                        Text('Resultados'),
                        txt_aposentadoria_reprovada,
                        txt_aposentadoria_aprovada,
                        txt_valor_beneficio,
                        txt_alerta
                    ]
                )
            )

        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    page.on_view_pop = voltar
    page.on_route_change = gerenciar_rotas
    page.go(page.route)

    def verificar_campos(e):
        try:
            int(media_salarial.value)
            int(idade.value)
            int(tempo_contribuicao.value)

            if meu_genero.value is None or idade.error or media_salarial.error or tempo_contribuicao.error or opcao.value is None:
                raise ValueError
            else:
                page.go('/resultados')
        except ValueError:
            print('')
            txt_alerta.value = 'Preencha os campos corretamente'
            page.update()

    def limpar_txt_alerta(e):
        txt_alerta.value = ''
        page.update()

    def calcular_beneficio():
        try:
            genero = meu_genero.value
            idade_var = int(idade.value)
            salario = int(media_salarial.value)
            tempo_contribuicao_var = int(tempo_contribuicao.value)
            categoria = opcao.value

            if genero == 'masculino':
                if categoria == 'idade':
                    if idade_var >= 65 and tempo_contribuicao_var >= 15:
                        txt_aposentadoria_aprovada.value = 'APROVADO'
                        v = salario * (0.6 + 0.02 * (tempo_contribuicao_var - 15))
                        txt_valor_beneficio.value = v
                    elif idade_var < 65 and tempo_contribuicao_var < 15:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (tempo e idade)'
                    elif idade_var < 65 and tempo_contribuicao_var >= 15:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (idade)'
                    else:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (tempo)'
                else:
                    if tempo_contribuicao_var >= 35:
                        txt_aposentadoria_aprovada.value = 'APROVADO'
                        v = salario * (0.6 + 0.02 * (tempo_contribuicao_var - 35))
                        txt_valor_beneficio.value = v
                    else:
                        txt_aposentadoria_reprovada.value = 'REPROVADO'
            elif genero == 'feminino':
                if categoria == 'idade':
                    if idade_var >= 62 and tempo_contribuicao_var >= 15:
                        txt_aposentadoria_aprovada.value = 'APROVADO'
                        v = salario * (0.6 + 0.02 * (tempo_contribuicao_var - 15))
                        txt_valor_beneficio.value = v
                    elif idade_var < 62 and tempo_contribuicao_var < 15:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (tempo e idade)'
                    elif idade_var < 62 and tempo_contribuicao_var >= 15:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (idade)'
                    else:
                        txt_aposentadoria_reprovada.value = 'REPROVADO (tempo)'
                else:
                    if tempo_contribuicao_var >= 30:
                        txt_aposentadoria_aprovada.value = "APROVADO"
                        v = salario * (0.6 + 0.02 * (tempo_contribuicao_var - 30))
                        txt_valor_beneficio.value = v
                    else:
                        txt_aposentadoria_reprovada.value = "REPROVADO"

        except ValueError:
            txt_alerta.value = 'Preencha os campos corretamente'
        page.update()

    idade = ft.TextField(label='informe quantos anos vc tem',
                         border_color=Colors.CYAN,
                         border_width=2,
                         border_radius=10,
                         focused_border_color=Colors.RED,
                         on_click=limpar_txt_alerta
                         )
    tempo_contribuicao = ft.TextField(label="tempo contribuição", hint_text="quantos anos voce trabalhou", on_click=limpar_txt_alerta)
    inss = ft.Image(src="inss.png")
    meu_genero = ft.Dropdown(
        label="Menu genero",
        width=page.window.width,
        fill_color=Colors.RED,
        border_radius=60,
        on_change=limpar_txt_alerta,

        options=[
            Option(key='masculino', text='masculino'), Option(key='feminino', text='feminino')],

    )

    media_salarial = ft.TextField(label='Média salarial', border_color=Colors.CYAN, border_width=2,
                                  border_radius=10, focused_border_color=Colors.RED, on_click=limpar_txt_alerta)

    opcao = ft.RadioGroup(on_change=limpar_txt_alerta, content=ft.Row([
        ft.Radio(value='tempo', label="Tempo de contribuição"),
        ft.Radio(value='idade', label="Idade")
    ]))

    txt_alerta = ft.Text(value='', italic=True, color="pink", size=22, bgcolor="#191970")
    txt_aposentadoria_reprovada = ft.Text(value='', italic=True, color="red", size=22, bgcolor="cyan")
    txt_aposentadoria_aprovada = ft.Text(value='', italic=True, color="green", size=22, bgcolor="cyan")
    txt_valor_beneficio = ft.Text(value='', size=22, bgcolor="#191970", color="yellow")

ft.app(main)