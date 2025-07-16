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
  CustomPage := CreateCustomPage(wpWelcome, 'Informa��es Importantes', 'Leia as informa��es abaixo antes de continuar.');

  MemoText := TMemo.Create(CustomPage);
  MemoText.Parent := CustomPage.Surface;
  MemoText.ScrollBars := ssVertical;
  MemoText.ReadOnly := True;
  MemoText.WordWrap := True;
  MemoText.TabStop := False;
  MemoText.Text := 'Este programa n�o armazena nenhuma informac�o como Login, Senha ou dados sens�veis respeitando a LGPD' +
    ' e foi desenvolvido para abrir instalar o programa Client Mine, instalar TLaucher na vers�o 1.8.5, ' +
    'permitindo verificar o envio de dados para o site ScoreGame hospedado no "toltaltouch.github.io/scoregame_site/" e gerar o relat�rio no formato de Log. Ao utilizar este software, voc� concorda com os seguintes termos:' + #13#10#13#10 +
    '1. Uso Respons�vel: O programa deve ser utilizado apenas para fins legais e autorizados. O usu�rio � respons�vel por garantir que possui permiss�o Client Mine.' + #13#10#13#10 +
    '2. Limita��o de Responsabilidade: O desenvolvedor n�o se responsabiliza por quaisquer danos, perdas ou consequ�ncias decorrentes ao mal uso do programa, incluindo erros de otimiz��o do TLacuncher, erro de servidor, etc.' + #13#10#13#10 +
    '3. Privacidade e Seguran�a: O programa utiliza credenciais fornecidas pelo usu�rio para realizar login no sistema. O usu�rio � respons�vel por proteger suas credenciais.';
    
  MemoText.Top := 10;
  MemoText.Left := 10;
  MemoText.Width := CustomPage.SurfaceWidth - 20;
  MemoText.Height := CustomPage.SurfaceHeight - 20;

  TermsPage := CreateInputOptionPage(CustomPage.ID,
    'Termos de Uso',
    'Leia e aceite os Termos de Uso para continuar',
    'Voc� deve aceitar os Termos de Uso para instalar o programa.',
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
      MsgBox('Para instalar esse programa, � necess�rio aceitar os Termos de Uso.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;

  Result := True; // Permite que o usuário avance
end;

// O READEME.pdf DEVE SER ESPECIFICAMENTE DO PROGRAMA NO FORMATO PDF
[Run]
Filename: "{app}\_internal\README.pdf"; Description: "Abrir instruções do programa"; Flags: postinstall shellexec skipifsilent
