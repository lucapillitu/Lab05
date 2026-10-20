import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1200
    page.window.height = 850

# --- ALERT ---
    alert = AlertManager(page)

# --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "luca pillitu")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

# --- UI ELEMENTI ---

# Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

# TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

# ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

# Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno di acquisto")
    input_value = ft.TextField(value="0", width="70", label="valore: €",
                               text_align=ft.TextAlign.CENTER,input_filter=ft.NumbersOnlyInputFilter())

# --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

# --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

# Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    #def per il counter del valore monetario
    def inc_valore(e) :
        valore = int(input_value.value or 0)
        input_value.value = str(valore + 1)
        input_value.update()

    def dec_valore(e):
        valore = int(input_value.value or 0)
        if valore > 0:
            input_value.value = str(valore - 1)
            input_value.update()

    #def aggiungi strumento
    def aggiungi_strumento(e):
        tipo = (input_tipo.value or "").strip()# or returna "" che rappresenta False in bool
        marca = (input_marca.value or "").strip()
        if not tipo or not marca:
            alert.show_alert("❌ Inserisci tipo e marca dello strumento")
            return

        try:
            anno = int(input_anno.value)
            valore = float(input_value.value or 0)
        except ValueError:
            alert.show_alert("❌ L'anno di acquisto deve essere un numero intero")
            return
        if anno <= 0 or valore <= 0:
            alert.show_alert("❌ Anno e valore devono essere maggiori di zero")
            return

        deposito.aggiungi_strumento(tipo, marca, anno, valore)
        #rimette a 0 i valori dopo l'inserimento
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_value.value = "0"
        aggiorna_lista_strumenti()




# --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)


# Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=dec_valore,icon_color="green")
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=inc_valore,icon_color="red")
    pulsante_aggiungi = ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_strumento)
# --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,

        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni sul Responsabile", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(controls=[input_tipo, input_marca, input_anno,pulsante_meno, input_value, pulsante_piu],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_aggiungi],
               alignment=ft.MainAxisAlignment.CENTER),
        # Sezione 4
        ft.Divider(),

        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
