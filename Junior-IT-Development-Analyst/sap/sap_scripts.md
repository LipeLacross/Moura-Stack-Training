# SAP Scripts - Automação de Processos no SAP

## Visão Geral
Scripts para automatizar tarefas repetitivas no SAP GUI usando SAP Scripting (VBScript).

## Pré-requisitos
1. SAP GUI 7.5+ instalado
2. SAP Scripting habilitado (transação RZ11)
3. Conexão com o servidor SAP

## Script 1: Extrair Relatório de Vendas

```vbscript
' Extrair relatório de vendas do SAP para CSV
' Transação: ZSD_REPORT

If Not IsObject(Application) Then
   Set SapGuiAuto = GetObject("SAPGUI")
   Set Application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(Connection) Then
   Set Connection = Application.Children(0)
End If
If Not IsObject(Session) Then
   Set Session = Connection.Children(0)
End If

' Acessar transação
Session.findById("wnd[0]").maximize
Session.findById("wnd[0]/tbar[0]/okcd").text = "/nZSD_REPORT"
Session.findById("wnd[0]").sendVKey 0

' Preencher parâmetros
Session.findById("wnd[0]/usr/ctxtS_VKORG-LOW").text = "1000"  ' Organização de Vendas
Session.findById("wnd[0]/usr/ctxtS_FKDAT-LOW").text = "20240101"  ' Data início
Session.findById("wnd[0]/usr/ctxtS_FKDAT-HIGH").text = "20241231"  ' Data fim

' Executar
Session.findById("wnd[0]/tbar[1]/btn[8]").press

' Exportar para arquivo
Session.findById("wnd[0]/tbar[0]/btn[45]").press
Session.findById("wnd[1]/usr/subSUBSCREEN:SAPLSLVC_DIALOG:0201/cmbG_USER-CRITERIA").key = "1"
Session.findById("wnd[1]/tbar[0]/btn[0]").press
Session.findById("wnd[1]/usr/ctxtDY_PATH").text = "C:\temp\"
Session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "relatorio_vendas_sap.csv"
Session.findById("wnd[1]/tbar[0]/btn[11]").press
```

## Script 2: Criar Ordem de Produção

```vbscript
' Criar ordem de produção no SAP
' Transação: CO01

Session.findById("wnd[0]/tbar[0]/okcd").text = "/nCO01"
Session.findById("wnd[0]").sendVKey 0

' Preencher dados da ordem
Session.findById("wnd[0]/usr/ctxtCAUFVD-AUFNR").text = ""  ' Número da ordem (deixar vazio para auto)
Session.findById("wnd[0]/usr/ctxtCAUFVD-WERKS").text = "1000"  ' Centro
Session.findById("wnd[0]/usr/ctxtRC27I-FLG_SEL").text = "X"    ' Selecionar material
Session.findById("wnd[0]/usr/ctxtCAUFVD-MATNR").text = "BAT-001"  ' Código do material
Session.findById("wnd[0]/usr/ctxtCAUFVD-GAMNG").text = "500"    ' Quantidade

' Salvar
Session.findById("wnd[0]/tbar[0]/btn[11]").press
```

## Script 3: Consultar Status de Pedido

```vbscript
' Consultar status de pedido de venda
' Transação: VA03

Session.findById("wnd[0]/tbar[0]/okcd").text = "/nVA03"
Session.findById("wnd[0]").sendVKey 0

Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = pedidoId
Session.findById("wnd[0]").sendVKey 0

' Extrair status
statusPedido = Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4020/txtVBUP-GBSTA").text
dataEntrega = Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4020/txtVBEP-EDATU").text
valorTotal = Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4020/txtVBAP-NETWR").text
```

## Boas Práticas

1. **Sempre validar** se a sessão SAP está ativa antes de executar
2. **Tratar erros** com `On Error Resume Next`
3. **Logar operações** em arquivo texto ou banco
4. **Usar variáveis de ambiente** para credenciais (nunca hard-coded)
5. **Agendar execução** via Windows Task Scheduler

## Integração com Python
```python
import subprocess

def executar_script_sap(script_path: str):
    result = subprocess.run(
        ["cscript", "//nologo", script_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return {"status": "ok", "output": result.stdout}
    return {"status": "error", "message": result.stderr}

# Exemplo de uso
resultado = executar_script_sap("sap/scripts/extrair_vendas.vbs")
```
