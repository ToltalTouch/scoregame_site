[Setup]
AppName= Client Mine
AppVersion=1.1.0
DefaultDirName={localappdata}\Client Mine
DefaultGroupName=Client Mine
OutputBaseFilename=ClientMine-Setup

Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "C:\minescore_project\disc_bot\dist\client_mine\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Icons]
Name: "{userdesktop}\Client Mine"; Filename: "{app}client_mine.exe"   
Name: "{userdesktop}\Desinstalar Client Mine"; Filename: "{uninstallexe}"

[Code]
var
  CustomPage: TWizardPage;
  TermsPage: TInputOptionWizardPage;
  MemoText: TMemo;

procedure InitializeWizard;
begin
  CustomPage := CreateCustomPage(wpWelcome, 'Informações Importantes', 'Leia as informações abaixo antes de continuar.');

  MemoText := TMemo.Create(CustomPage);
  MemoText.Parent := CustomPage.Surface;
  MemoText.ScrollBars := ssVertical;
  MemoText.ReadOnly := True;
  MemoText.WordWrap := True;
  MemoText.TabStop := False;
  MemoText.Text := 'Este programa não armazena nenhuma informacão como Login, Senha ou dados sensíveis respeitando a LGPD' +
    ' e foi desenvolvido para abrir instalar o programa Client Mine, instalar TLaucher na versão 1.8.5, ' +
    'permitindo verificar o envio de dados para o site ScoreGame hospedado no "toltaltouch.github.io/scoregame_site/" e gerar o relatório no formato de Log. Ao utilizar este software, você concorda com os seguintes termos:' + #13#10#13#10 +
    '1. Uso Responsável: O programa deve ser utilizado apenas para fins legais e autorizados. O usuário é responsável por garantir que possui permissão Client Mine.' + #13#10#13#10 +
    '2. Limitação de Responsabilidade: O desenvolvedor não se responsabiliza por quaisquer danos, perdas ou consequências decorrentes ao mal uso do programa, incluindo erros de otimizção do TLacuncher, erro de servidor, etc.' + #13#10#13#10 +
    '3. Privacidade e Segurança: O programa utiliza credenciais fornecidas pelo usuário para realizar login no sistema. O usuário é responsável por proteger suas credenciais.';
    
  MemoText.Top := 10;
  MemoText.Left := 10;
  MemoText.Width := CustomPage.SurfaceWidth - 20;
  MemoText.Height := CustomPage.SurfaceHeight - 20;

  TermsPage := CreateInputOptionPage(CustomPage.ID,
    'Termos de Uso',
    'Leia e aceite os Termos de Uso para continuar',
    'Você deve aceitar os Termos de Uso para instalar o programa.',
    True, False);

  TermsPage.Add('Eu li e aceito os Termos de Uso.');

  TermsPage.Values[0] := False;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if CurPageID = TermsPage.ID then
  begin

    if not TermsPage.Values[0] then
    begin
      MsgBox('Para instalar esse programa, é necessário aceitar os Termos de Uso.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;

  Result := True; // Permite que o usuÃ¡rio avance
end;

// O READEME.pdf DEVE SER ESPECIFICAMENTE DO PROGRAMA NO FORMATO PDF
[Run]
Filename: "{app}\_internal\README.pdf"; Description: "Abrir instruÃ§Ãµes do programa"; Flags: postinstall shellexec skipifsilent
