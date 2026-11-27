Attribute VB_Name = "ExcelShapesDrawingWithJSON"
''
' Excel Shapes Drawing Program to active sheet with Flowchart JSON Data (macOS, Beta Version)
' Version 2026.06.18
' (c) Toshiki Yoshino - https://github.com/YoshiToshi1025/flowchart-drawing-tool-python
'
' @author Toshiki Yoshino
' @license MIT (http://www.opensource.org/licenses/mit-license.php)
'==============================================================

Option Explicit

'==============================================================
' ƒtƒ[ƒ`ƒƒ[ƒg JSON ¨ Excel •`‰æƒ}ƒNƒ
' Excel VBA for Microsoft 365
'
' JSONƒtƒ@ƒCƒ‹‚É’è‹`‚³‚ê‚½ƒtƒ[ƒ`ƒƒ[ƒgƒf[ƒ^iƒm[ƒhEƒGƒbƒWE
' ƒXƒCƒ€ƒŒ[ƒ“j‚ğ“Ç‚İ‚İAƒAƒNƒeƒBƒuƒV[ƒg‚É•`‰æ‚·‚éB
'==============================================================

' ============================================================
' ƒf[ƒ^\‘¢’è‹`
' ============================================================

' ƒm[ƒg(•tâ³)î•ñ
Private Type NoteData
    dx           As Double  ' ƒ‰ƒxƒ‹‚ÌxÀ•W(pt)iƒm[ƒh’†S‚©‚ç‚Ì‘Š‘ÎˆÊ’uj
    dy           As Double  ' ƒ‰ƒxƒ‹‚ÌyÀ•W(pt)iƒm[ƒh’†S‚©‚ç‚Ì‘Š‘ÎˆÊ’uj
    displayState As String  ' •\¦ó‘Ô: normal/hidden(ƒ}ƒNƒ‚Å‚ÍA•\¦ó‘Ô‚ÉŠÖŒW‚È‚­í‚É•\¦)
    w            As Double  ' * •(pt)
    h            As Double  ' * ‚‚³(pt)
End Type

' ƒm[ƒhi—v‘fjî•ñ
Private Type NodeData
    id        As Long       ' —v‘fID
    cellText  As String     ' ƒ‰ƒxƒ‹ƒeƒLƒXƒg
    nodeType  As String     ' ƒm[ƒhí—Ş terminator/process/decision/io/storage/document/special_node
    shapeType As String     ' Œ`ó connector/terminator/rectangle/corner_rounded_rectangle/rounded_rectangle
    status    As String     ' ƒXƒe[ƒ^ƒX normal/active/inactive
    
    x         As Double     ' ’†SxÀ•W(pt)
    y         As Double     ' ’†SyÀ•W(pt)
    w         As Double     ' •(pt)
    h         As Double     ' ‚‚³(pt)
    
    fillColor As String     ' “h‚è‚Â‚Ô‚µF "#rrggbb"
    outlineColor As String  ' * ‰æ‚èF "#rrggbb"
    outlineWidth As Double  ' * ‰æ‚èü‚Ì‘¾‚³(pt)
    textWidth As Double     ' * ƒeƒLƒXƒgƒGƒŠƒA‚Ì•
    textColor As String     ' * ƒeƒLƒXƒgF "#rrggbb"
    fontFamily As String    ' * ƒtƒHƒ“ƒgí—Ş
    fontSize  As Double     ' * ƒtƒHƒ“ƒgƒTƒCƒY(pt)
    fontWeight As String    ' * ƒtƒHƒ“ƒgƒEƒFƒCƒg normal/bold
    details   As String     ' Ú×î•ñ
    
    note      As NoteData   ' ƒm[ƒgî•ñ

    shapeName As String     ' ExcelƒVƒFƒCƒv–¼iƒGƒbƒWÚ‘±—pj
    noteShapeName As String ' ƒm[ƒgƒVƒFƒCƒv–¼iÅ‘O–Ê‚Ö‚ÌˆÚ“®—pj
    noteConnName As String  ' ƒm[ƒg‚Ö‚ÌƒŠƒ“ƒN–¼iÅ‘O–Ê‚Ö‚ÌˆÚ“®—pj
End Type

' ƒGƒbƒWiƒŠƒ“ƒNjî•ñ
Private Type EdgeData
    id             As Long     ' * ƒŠƒ“ƒNID@¦–¢g—p
    edgeLabel      As String   ' ƒ‰ƒxƒ‹ƒeƒLƒXƒg
    fromId         As Long     ' from‘¤ƒm[ƒhID
    toId           As Long     ' to‘¤ƒm[ƒhID
    edgeType       As String   ' elbow, line
    pathType       As String   ' * ƒŠƒ“ƒNÚ‘±ƒpƒX vertical/horizontal/tree ¦–¢g—p
    lineStyle      As String   ' solid, dotted, dashed
    lineColor      As String   ' * üF "#rrggbb"
    lineWidth      As Double   ' * ü‚Ì‘¾‚³(pt)
    arrowKind      As String   ' * –îˆó‚Ìí—Ş last/first/both/none
    
    connMode       As String   ' ©“®Ú‘±? auto/manual
    fromCP         As String   ' Ú‘±“_ top/left/bottom/right/""(auto)   auto‚Í”p~—\’è
    toCP           As String   ' Ú‘±“_ top/left/bottom/right/""(auto)   auto‚Í”p~—\’è
    edgeWrapMargin As Double   ' ƒGƒbƒW‰ñ‚è‚İ‹——£(pt) ¦–¢‘Î‰
    edgeWrapRatio1 As Double   ' Item1‚ÌƒGƒbƒW‰ñ‚è‚İŠ„‡
    edgeWrapRatio2 As Double   ' Item2‚ÌƒGƒbƒW‰ñ‚è‚İŠ„‡
    
    labelPos       As String   ' ƒ‰ƒxƒ‹ˆÊ’u auto/p2se/posw/p0nw/p0ne/p1se/....
    labelX         As Double   ' ƒ‰ƒxƒ‹xÀ•W(pt)
    labelY         As Double   ' ƒ‰ƒxƒ‹yÀ•W(pt)
    labelAnchor    As String   ' ƒ‰ƒxƒ‹Šî€ˆÊ’u center/n/ne/e/se/s/sw/w/nw
    labelJustify   As String   ' Šî€ˆÊ’u‚É‚¨‚¯‚éƒ‰ƒxƒ‹”z’uˆÊ’u left/center/right

    textWidth      As Double   ' * ƒeƒLƒXƒgƒGƒŠƒA‚Ì•
    textColor      As String   ' * ƒeƒLƒXƒgF "#rrggbb"
    fontFamily     As String   ' * ƒtƒHƒ“ƒgí—Ş
    fontSize       As Double   ' * ƒtƒHƒ“ƒgƒTƒCƒY(pt)
    fontWeight     As String   ' * ƒtƒHƒ“ƒgƒEƒFƒCƒg normal/bold
End Type

' ƒXƒCƒ€ƒŒ[ƒ“î•ñ
Private Type SwimlaneData
    kind      As String    ' vertical, horizontal
    title     As String    ' ƒwƒbƒ_[/ƒtƒbƒ^[ƒeƒLƒXƒg
    headerCX  As Double    ' ƒwƒbƒ_[’†Sx(pt)
    headerCY  As Double    ' ƒwƒbƒ_[’†Sy(pt)
    width     As Double    ' –{‘Ì•(pt)
    height    As Double    ' –{‘Ì‚‚³(pt)
    fillColor As String    ' “h‚è‚Â‚Ô‚µF "#rrggbb"
    outlineColor As String ' * ‰æ‚èF "#rrggbb"
    textColor As String    ' * ƒeƒLƒXƒgF "#rrggbb"
    
    groupName As String    ' ƒOƒ‹[ƒvƒVƒFƒCƒv–¼iZ-order’²®—pj
End Type

' ============================================================
' JSON‰ğÍ—pƒOƒ[ƒoƒ‹•Ï”
' ============================================================
Private gJson As String   ' ‰ğÍ‘ÎÛJSON•¶š—ñ
Private gPos  As Long     ' Œ»İ‚Ì‰ğÍˆÊ’u

' ============================================================
' ƒpƒ‰ƒ[ƒ^
' ============================================================
Public PointPerPixel As Double  ' 1ƒsƒNƒZƒ‹‚ ‚½‚è‚Ìƒ|ƒCƒ“ƒg’liOS‚âŠÂ‹«‚ÅˆÙ‚È‚éj
Public BackSlash As String      ' ƒoƒbƒNƒXƒ‰ƒbƒVƒ…•¶šiWindows‚ÆmacOS‚ÅˆÙ‚È‚éj


' ============================================================
' ƒGƒ“ƒgƒŠ[ƒ|ƒCƒ“ƒg
' ============================================================
Public Sub DrawFlowchart()

    #If Mac Then
        PointPerPixel = 1#    ' macOS‚Å‚Í1.0‚É
        BackSlash = "€"
    #Else
        PointPerPixel = 0.75  ' Windows‚Å‚Í0.75‚É
        BackSlash = "\"
    #End If
    
    ' --- JSONƒtƒ@ƒCƒ‹‘I‘ğ ---
    Dim filePath As String
    #If Mac Then
        filePath = GetJsonFilePathForMacOS()
    #Else
        filePath = GetJsonFilePath()
    #End If
    If filePath = "" Then Exit Sub

    ' --- ƒtƒ@ƒCƒ‹“Ç‚İ‚İ ---
    Dim jsonText As String
    #If Mac Then
        jsonText = ReadUTF8FileForMacOS(filePath)
    #Else
        jsonText = ReadTextFile(filePath)
    #End If
    If jsonText = "" Then
        MsgBox "Failed to load the file. / ƒtƒ@ƒCƒ‹‚Ì“Ç‚İ‚İ‚É¸”s‚µ‚Ü‚µ‚½B" & vbCrLf & filePath, vbCritical, "Error"
        Exit Sub
    End If

    ' --- •`‰ææƒV[ƒg ---
    Dim ws As Worksheet
    Set ws = ActiveSheet

    ' --- ƒf[ƒ^”z—ñ ---
    Dim nodes()     As NodeData
    Dim edges()     As EdgeData
    Dim swimlanes() As SwimlaneData
    Dim nCount As Long, eCount As Long, sCount As Long
    nCount = 0: eCount = 0: sCount = 0

    On Error GoTo ErrHandler
    Application.ScreenUpdating = False

    ' --- ƒCƒ“ƒ|[ƒg‘O‚Ì}Œ`‚ğŒŸ’m ---
    Dim preShapesCounter As Integer
    preShapesCounter = CountGroupableShapes()
    ' MsgBox "preShapesCounter : " & preShapesCounter

    ' --- JSON‰ğÍ ---
    Call ParseFlowchartJson(jsonText, nodes, edges, swimlanes, nCount, eCount, sCount)

    ' --- •`‰æiZ-order: ƒXƒCƒ€ƒŒ[ƒ“ ¨ ƒGƒbƒW ¨ ƒm[ƒh ‚Ì‡‚ÅÅ‘O–Êj---
    ' •`‰æ‡: ƒXƒCƒ€ƒŒ[ƒ“ ¨ ƒm[ƒh ¨ ƒGƒbƒWiŒã‚ÅZ-order’²®j
    Call DrawSwimlanes(ws, swimlanes, sCount)
    Call DrawNodes(ws, nodes, nCount)
    Call DrawEdges(ws, edges, eCount, nodes, nCount)
    Call AdjustZOrder(ws, nodes, nCount, swimlanes, sCount)

    If preShapesCounter = 0 Then
        Call GroupAllGroupableShapes
    End If

    Application.ScreenUpdating = True
    
    If preShapesCounter = 0 Then
        MsgBox "Excel Shapes Drawing" & vbCrLf & _
               "  Nodes     : " & nCount & vbCrLf & _
               "  Edges     : " & eCount & vbCrLf & _
               "  Swimlanes : " & sCount & vbCrLf & vbCrLf & _
               "  [Message] Shapes have been successfully grouped.", vbInformation, "Flowchart Drawing"
        Exit Sub
    Else
        MsgBox "Excel Shapes Drawing" & vbCrLf & _
               "  Nodes     : " & nCount & vbCrLf & _
               "  Edges     : " & eCount & vbCrLf & _
               "  Swimlanes : " & sCount & vbCrLf & vbCrLf & _
               "  [Warning] Shape grouping was skipped because existing shapes were detected.", vbInformation, "Flowchart Drawing"
        Exit Sub
    End If

ErrHandler:
    Application.ScreenUpdating = True
    MsgBox "An error occurred. / ƒGƒ‰[‚ª”­¶‚µ‚Ü‚µ‚½B" & vbCrLf & _
           "Description: " & Err.Description & vbCrLf & _
           "Error No.  : " & Err.Number, vbCritical, "Error"
End Sub

' ============================================================
' ƒtƒ@ƒCƒ‹‘€ì
' ============================================================

' ƒtƒ@ƒCƒ‹ƒ_ƒCƒAƒƒO‚ÅJSONƒtƒ@ƒCƒ‹ƒpƒX‚ğæ“¾
Private Function GetJsonFilePath() As String
    With Application.FileDialog(msoFileDialogFilePicker)
        .title = "Please select a JSON file. / JSONƒtƒ@ƒCƒ‹‚ğ‘I‘ğ‚µ‚Ä‚­‚¾‚³‚¢"
        .Filters.Clear
        .Filters.Add "JSON File", "*.json"
        .Filters.Add "All", "*.*"
        .AllowMultiSelect = False
        If .Show Then
            GetJsonFilePath = .SelectedItems(1)
        End If
    End With
End Function

' ƒeƒLƒXƒgƒtƒ@ƒCƒ‹‚ğUTF-8‚Å“Ç‚İ‚ŞiADODB.Streamg—pj
Private Function ReadTextFile(filePath As String) As String
    On Error GoTo FallbackRead
    ' ADODB.Stream ‚ÅUTF-8“Ç‚İ‚İ‚ğ‚İ‚é
    Dim stm As Object
    Set stm = CreateObject("ADODB.Stream")
    stm.Type = 2          ' adTypeText
    stm.Charset = "UTF-8"
    stm.Open
    stm.LoadFromFile filePath
    ReadTextFile = stm.ReadText
    stm.Close
    Set stm = Nothing
    Exit Function

FallbackRead:
    ' ƒtƒH[ƒ‹ƒoƒbƒN: ’Êí‚Ìƒtƒ@ƒCƒ‹“ü—Í
    On Error GoTo 0
    Dim fNum As Integer
    Dim ln   As String
    Dim buf  As String
    fNum = FreeFile()
    Open filePath For Input As #fNum
    buf = ""
    Do While Not EOF(fNum)
        Line Input #fNum, ln
        buf = buf & ln & Chr(10)
    Loop
    Close #fNum
    ReadTextFile = buf
End Function

' ============================================================
' JSON ƒp[ƒT[iƒƒCƒ“j
' ============================================================

' JSONƒeƒLƒXƒg‚ğ‰ğÍ‚µ‚Äƒm[ƒhEƒGƒbƒWEƒXƒCƒ€ƒŒ[ƒ“‚ğ”z—ñ‚ÉŠi”[‚·‚é
Private Sub ParseFlowchartJson(jsonText As String, _
    nodes() As NodeData, edges() As EdgeData, swimlanes() As SwimlaneData, _
    nCount As Long, eCount As Long, sCount As Long)

    gJson = jsonText
    gPos = 1

    ' \•ª‚È”z—ñƒTƒCƒY‚ğŠm•Û
    ReDim nodes(0 To 499)
    ReDim edges(0 To 999)
    ReDim swimlanes(0 To 99)

    Dim key As String
    Dim c   As String

    SkipWS
    ExpectCh "{"

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c <> """" Then Exit Do

        key = JsonStr()
        SkipWS
        ExpectCh ":"
        SkipWS

        Select Case key
            Case "nodes"
                Call ParseNodesArr(nodes, nCount)
            Case "edges"
                Call ParseEdgesArr(edges, eCount)
            Case "swimlanes"
                Call ParseSwimlanesArr(swimlanes, sCount)
            Case Else
                Call JsonSkip
        End Select
    Loop
End Sub

' ============================================================
' ƒm[ƒh”z—ñEƒIƒuƒWƒFƒNƒg‰ğÍ
' ============================================================

Private Sub ParseNodesArr(nodes() As NodeData, nCount As Long)
    Dim c As String
    ExpectCh "["
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If

        If c = "{" Then
            Call ParseNodeObj(nodes(nCount))
            nCount = nCount + 1
        Else
            Call JsonSkip
        End If
    Loop
End Sub

Private Sub ParseNodeObj(nd As NodeData)
    Dim key As String
    Dim c   As String

    ' ƒfƒtƒHƒ‹ƒg’l
    nd.shapeType = ""
    nd.status = "normal"
    nd.fillColor = "#ffffff"
    nd.outlineColor = "#334155"
    nd.outlineWidth = 2 * PointPerPixel
    nd.textWidth = 110 * PointPerPixel
    nd.textColor = "#0f172a"
    nd.fontFamily = "Arial"
    nd.fontSize = 9
    nd.fontWeight = "normal"
    
    Dim terminator_fillColor As String
    terminator_fillColor = "#e0e0e0"

    ExpectCh "{"
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c <> """" Then Exit Do

        key = JsonStr()
        SkipWS
        ExpectCh ":"
        SkipWS

        Select Case key
            Case "id"
                nd.id = CLng(Val(JsonNum()))
            Case "text"
                nd.cellText = JsonStr()
            Case "type"
                nd.nodeType = JsonStr()
                If nd.nodeType = "terminator" Then
                    nd.fillColor = terminator_fillColor
                End If
            Case "shape_type"
                nd.shapeType = JsonStr()
            Case "status"
                nd.status = JsonStr()
            Case "x"
                nd.x = CDbl(Val(JsonNum())) * PointPerPixel
            Case "y"
                nd.y = CDbl(Val(JsonNum())) * PointPerPixel
            Case "w"
                nd.w = CDbl(Val(JsonNum())) * PointPerPixel
            Case "h"
                nd.h = CDbl(Val(JsonNum())) * PointPerPixel
            Case "fill_color"
                nd.fillColor = JsonStr()
            Case "outline_color"
                nd.outlineColor = JsonStr()
            Case "outline_width"
                nd.outlineWidth = CDbl(Val(JsonNum())) * PointPerPixel
            Case "text_width"
                nd.textWidth = CDbl(Val(JsonNum())) * PointPerPixel
            Case "text_color"
                nd.textColor = JsonStr()
            Case "font_family"
                nd.fontFamily = JsonStr()
            Case "font_size"
                nd.fontSize = CDbl(Val(JsonNum()))
            Case "font_weight"
                nd.fontWeight = JsonStr()
            Case "details"
                nd.details = JsonStr()
            Case "note"
                Call ParseNoteObj(nd.note)
            Case Else
                Call JsonSkip
        End Select
    Loop
    
    If nd.shapeType = "" Then
        Select Case LCase(nd.nodeType)
            Case "terminator"
                If nd.w <= 45 Then
                    nd.shapeType = "connector"
                Else
                    nd.shapeType = "terminator"
                End If
            Case "process"
                nd.shapeType = "corner_rounded_rectangle"
            Case Else
                nd.shapeType = ""
        End Select
    End If
End Sub

Private Sub ParseNoteObj(note As NoteData)
    Dim key As String
    Dim c   As String

    ' ƒfƒtƒHƒ‹ƒg’l
    note.dx = 0
    note.dy = 0
    note.displayState = "normal"
    note.w = 150 * PointPerPixel
    note.h = 135 * PointPerPixel

    ExpectCh "{"
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c <> """" Then Exit Do

        key = JsonStr()
        SkipWS
        ExpectCh ":"
        SkipWS

        Select Case key
            Case "dx"
                note.dx = CDbl(Val(JsonNum())) * PointPerPixel
            Case "dy"
                note.dy = CDbl(Val(JsonNum())) * PointPerPixel
            Case "display_state"
                note.displayState = JsonStr()
            Case "w"
                note.w = CDbl(Val(JsonNum())) * PointPerPixel
            Case "h"
                note.h = CDbl(Val(JsonNum())) * PointPerPixel
            Case Else
                Call JsonSkip
        End Select
    Loop
End Sub

' ============================================================
' ƒGƒbƒW”z—ñEƒIƒuƒWƒFƒNƒg‰ğÍ
' ============================================================

Private Sub ParseEdgesArr(edges() As EdgeData, eCount As Long)
    Dim c As String
    ExpectCh "["
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If

        If c = "{" Then
            Call ParseEdgeObj(edges(eCount))
            eCount = eCount + 1
        Else
            Call JsonSkip
        End If
    Loop
End Sub

Private Sub ParseEdgeObj(ed As EdgeData)
    Dim key As String
    Dim c   As String

    ' ƒfƒtƒHƒ‹ƒg’l
    ed.edgeLabel = ""
    ed.edgeType = "elbow"
    ed.pathType = "vertical"
    ed.lineStyle = "solid"
    ed.lineColor = "#0f172a"
    ed.lineWidth = 2 * PointPerPixel
    ed.arrowKind = "last"

    ed.connMode = "auto"
    ed.fromCP = ""
    ed.toCP = ""
    ed.labelPos = "auto"
    ed.labelAnchor = "center"
    ed.labelJustify = "left"
    
    ed.textWidth = 200 * PointPerPixel
    ed.textColor = "#0f172a"
    ed.fontFamily = "Arial"
    ed.fontSize = 9
    ed.fontWeight = "normal"

    ExpectCh "{"
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c <> """" Then Exit Do

        key = JsonStr()
        SkipWS
        ExpectCh ":"
        SkipWS

        Select Case key
            Case "id"
                ed.id = CLng(Val(JsonNum()))
            Case "label"
                ed.edgeLabel = JsonStr()
            Case "from_id"
                ed.fromId = CLng(Val(JsonNum()))
            Case "to_id"
                ed.toId = CLng(Val(JsonNum()))
            Case "edge_type"
                ed.edgeType = JsonStr()
            Case "path_type"
                ed.pathType = JsonStr()
            Case "line_style"
                ed.lineStyle = JsonStr()
            Case "color"                    ' ‹Œ—v‘f–¼‚Ö‚Ì‘Î‰
                ed.lineColor = JsonStr()
            Case "line_color"
                ed.lineColor = JsonStr()
            Case "line_width"
                ed.lineWidth = CDbl(Val(JsonNum())) * PointPerPixel
            Case "arrow_kind"
                ed.arrowKind = JsonStr()
            
            Case "connection_mode"
                ed.connMode = JsonStr()
            Case "from_connection_point"
                ed.fromCP = JsonStr()
            Case "to_connection_point"
                ed.toCP = JsonStr()
            Case "edge_wrap_margin"
                ed.edgeWrapMargin = CDbl(Val(JsonNum())) * PointPerPixel
            Case "edge_wrap_ratio1"
                ed.edgeWrapRatio1 = CDbl(Val(JsonNum()))
            Case "edge_wrap_ratio2"
                ed.edgeWrapRatio2 = CDbl(Val(JsonNum()))
            
            Case "label_position"
                ed.labelPos = JsonStr()
            Case "label_x"
                ed.labelX = CDbl(Val(JsonNum())) * PointPerPixel
            Case "label_y"
                ed.labelY = CDbl(Val(JsonNum())) * PointPerPixel
            Case "label_anchor"
                ed.labelAnchor = JsonStr()
            Case "label_justify"
                ed.labelJustify = JsonStr()
            
            Case "text_width"
                ed.textWidth = CDbl(Val(JsonNum())) * PointPerPixel
            Case "text_color"
                ed.textColor = JsonStr()
            Case "font_family"
                ed.fontFamily = JsonStr()
            Case "font_size"
                ed.fontSize = CDbl(Val(JsonNum()))
            Case "font_weight"
                ed.fontWeight = JsonStr()
            
            Case Else
                Call JsonSkip
        End Select
    Loop
End Sub

' ============================================================
' ƒXƒCƒ€ƒŒ[ƒ“”z—ñEƒIƒuƒWƒFƒNƒg‰ğÍ
' ============================================================

Private Sub ParseSwimlanesArr(swimlanes() As SwimlaneData, sCount As Long)
    Dim c As String
    ExpectCh "["
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "]" Then
            gPos = gPos + 1
            Exit Do
        End If

        If c = "{" Then
            Call ParseSwimlaneObj(swimlanes(sCount))
            sCount = sCount + 1
        Else
            Call JsonSkip
        End If
    Loop
End Sub

Private Sub ParseSwimlaneObj(sw As SwimlaneData)
    Dim key As String
    Dim c   As String

    ' ƒfƒtƒHƒ‹ƒg’l
    sw.fillColor = "#e0e0e0"
    sw.outlineColor = "#808080"
    sw.textColor = "#0f172a"
    
    ExpectCh "{"
    SkipWS

    Do While gPos <= Len(gJson)
        SkipWS
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c = "," Then
            gPos = gPos + 1
            SkipWS
        End If
        If gPos > Len(gJson) Then Exit Do
        c = Mid(gJson, gPos, 1)
        If c = "}" Then
            gPos = gPos + 1
            Exit Do
        End If
        If c <> """" Then Exit Do

        key = JsonStr()
        SkipWS
        ExpectCh ":"
        SkipWS

        Select Case key
            Case "kind"
                sw.kind = JsonStr()
            Case "title"
                sw.title = JsonStr()
            Case "header_center_x"
                sw.headerCX = CDbl(Val(JsonNum())) * PointPerPixel
            Case "header_center_y"
                sw.headerCY = CDbl(Val(JsonNum())) * PointPerPixel
            Case "width"
                sw.width = CDbl(Val(JsonNum())) * PointPerPixel
            Case "height"
                sw.height = CDbl(Val(JsonNum())) * PointPerPixel
            Case "fill_color"
                sw.fillColor = JsonStr()
            Case Else
                Call JsonSkip
        End Select
    Loop
End Sub

' ============================================================
' JSON ’áƒŒƒxƒ‹ƒp[ƒT[iš‹å‰ğÍj
' ============================================================

' ‹ó”’E‰üs‚ğƒXƒLƒbƒv
Private Sub SkipWS()
    Dim c As String
    Do While gPos <= Len(gJson)
        c = Mid(gJson, gPos, 1)
        If c = " " Or c = Chr(9) Or c = Chr(10) Or c = Chr(13) Then
            gPos = gPos + 1
        Else
            Exit Do
        End If
    Loop
End Sub

' w’è•¶š‚ğÁ”ïiˆê’v‚µ‚È‚¢ê‡‚Í‰½‚à‚µ‚È‚¢j
Private Sub ExpectCh(c As String)
    If gPos <= Len(gJson) Then
        If Mid(gJson, gPos, 1) = c Then gPos = gPos + 1
    End If
End Sub

' JSON•¶š—ñ‚ğ‰ğÍ‚µ‚Ä•Ô‚·iƒGƒXƒP[ƒvˆ—ŠÜ‚Şj
Private Function JsonStr() As String
    Dim result As String
    Dim c      As String

    SkipWS
    If gPos > Len(gJson) Or Mid(gJson, gPos, 1) <> """" Then
        JsonStr = ""
        Exit Function
    End If
    gPos = gPos + 1  ' ŠJn " ‚ğƒXƒLƒbƒv

    result = ""
    Do While gPos <= Len(gJson)
        c = Mid(gJson, gPos, 1)
        If c = """" Then
            gPos = gPos + 1
            Exit Do
        ElseIf c = BackSlash Then
            gPos = gPos + 1
            If gPos > Len(gJson) Then Exit Do
            c = Mid(gJson, gPos, 1)
            Select Case c
                Case "n": result = result & Chr(10)    ' ‰üs
                Case "r": result = result & Chr(13)    ' CR
                Case "t": result = result & Chr(9)     ' ƒ^ƒu
                Case """": result = result & """"
                Case BackSlash: result = result & BackSlash
                Case "/": result = result & "/"
                Case Else: result = result & c
            End Select
            gPos = gPos + 1
        Else
            result = result & c
            gPos = gPos + 1
        End If
    Loop

    JsonStr = result
End Function

' JSON”’l‚ğ‰ğÍ‚µ‚Ä•¶š—ñ‚Å•Ô‚·
Private Function JsonNum() As String
    Dim start As Long
    Dim c     As String

    SkipWS
    start = gPos

    If gPos <= Len(gJson) And Mid(gJson, gPos, 1) = "-" Then gPos = gPos + 1

    Do While gPos <= Len(gJson)
        c = Mid(gJson, gPos, 1)
        If c >= "0" And c <= "9" Then gPos = gPos + 1 Else Exit Do
    Loop

    If gPos <= Len(gJson) And Mid(gJson, gPos, 1) = "." Then
        gPos = gPos + 1
        Do While gPos <= Len(gJson)
            c = Mid(gJson, gPos, 1)
            If c >= "0" And c <= "9" Then gPos = gPos + 1 Else Exit Do
        Loop
    End If

    ' w”•”
    If gPos <= Len(gJson) Then
        c = Mid(gJson, gPos, 1)
        If c = "e" Or c = "E" Then
            gPos = gPos + 1
            If gPos <= Len(gJson) Then
                c = Mid(gJson, gPos, 1)
                If c = "+" Or c = "-" Then gPos = gPos + 1
            End If
            Do While gPos <= Len(gJson)
                c = Mid(gJson, gPos, 1)
                If c >= "0" And c <= "9" Then gPos = gPos + 1 Else Exit Do
            Loop
        End If
    End If

    JsonNum = Mid(gJson, start, gPos - start)
End Function

' JSON’l‚ğ“Ç‚İ”ò‚Î‚·i–¢’m‚ÌƒL[‚Ì’l—pj
Private Sub JsonSkip()
    Dim c     As String
    Dim dummy As String

    SkipWS
    If gPos > Len(gJson) Then Exit Sub
    c = Mid(gJson, gPos, 1)

    Select Case c
        Case "{": Call JsonSkipObj
        Case "[": Call JsonSkipArr
        Case """": dummy = JsonStr()
        Case "t": gPos = gPos + 4   ' true
        Case "f": gPos = gPos + 5   ' false
        Case "n": gPos = gPos + 4   ' null
        Case Else: dummy = JsonNum()
    End Select
End Sub

Private Sub JsonSkipObj()
    Dim depth As Long
    Dim c     As String
    Dim dummy As String

    ExpectCh "{"
    depth = 1

    Do While gPos <= Len(gJson) And depth > 0
        c = Mid(gJson, gPos, 1)
        Select Case c
            Case """": dummy = JsonStr()
            Case "{": depth = depth + 1: gPos = gPos + 1
            Case "}": depth = depth - 1: gPos = gPos + 1
            Case Else: gPos = gPos + 1
        End Select
    Loop
End Sub

Private Sub JsonSkipArr()
    Dim depth As Long
    Dim c     As String
    Dim dummy As String

    ExpectCh "["
    depth = 1

    Do While gPos <= Len(gJson) And depth > 0
        c = Mid(gJson, gPos, 1)
        Select Case c
            Case """": dummy = JsonStr()
            Case "[": depth = depth + 1: gPos = gPos + 1
            Case "]": depth = depth - 1: gPos = gPos + 1
            Case Else: gPos = gPos + 1
        End Select
    Loop
End Sub

' ============================================================
' •`‰æ: ƒXƒCƒ€ƒŒ[ƒ“
' ============================================================

Private Sub DrawSwimlanes(ws As Worksheet, swimlanes() As SwimlaneData, sCount As Long)
    Dim i As Long
    For i = 0 To sCount - 1
        Call DrawSwimlane(ws, swimlanes(i))
    Next i
End Sub

' ƒXƒCƒ€ƒŒ[ƒ“1‚Â‚ğ•`‰æi–{‘ÌEƒwƒbƒ_[Eƒtƒbƒ^[‚ğƒOƒ‹[ƒv‰»j
Private Sub DrawSwimlane(ws As Worksheet, sw As SwimlaneData)
    Dim HDR_SIZE As Double
    HDR_SIZE = 30 * PointPerPixel   ' ƒwƒbƒ_[/ƒtƒbƒ^[‚ÌŒÅ’èƒTƒCƒY(pt)

    Dim bodyL As Double, bodyT As Double
    Dim bodyW As Double, bodyH As Double
    Dim hdrL  As Double, hdrT As Double, hdrW As Double, hdrH As Double
    Dim ftrL  As Double, ftrT As Double, ftrW As Double, ftrH As Double
    Dim isHoriz As Boolean

    bodyW = sw.width
    bodyH = sw.height
    isHoriz = (LCase(sw.kind) = "horizontal")

    If Not isHoriz Then
        ' cŒ^: ƒwƒbƒ_[ã•”/ƒtƒbƒ^[‰º•”A•=–{‘Ì•A‚‚³=30
        hdrW = bodyW: hdrH = HDR_SIZE
        hdrL = sw.headerCX - hdrW / 2
        hdrT = sw.headerCY - hdrH / 2
        bodyL = hdrL: bodyT = hdrT          ' –{‘Ì¶ã = ƒwƒbƒ_[¶ã
        ftrL = bodyL: ftrT = bodyT + bodyH - HDR_SIZE
        ftrW = bodyW: ftrH = HDR_SIZE
    Else
        ' ‰¡Œ^: ƒwƒbƒ_[¶•”/ƒtƒbƒ^[‰E•”A•=30A‚‚³=–{‘Ì‚‚³
        hdrW = HDR_SIZE: hdrH = bodyH
        hdrL = sw.headerCX - hdrW / 2
        hdrT = sw.headerCY - hdrH / 2
        bodyL = hdrL: bodyT = hdrT          ' –{‘Ì¶ã = ƒwƒbƒ_[¶ã
        ftrL = bodyL + bodyW - HDR_SIZE: ftrT = bodyT
        ftrW = HDR_SIZE: ftrH = bodyH
    End If

    ' --- –{‘Ìi“h‚è‚Â‚Ô‚µ‚È‚µj ---
    Dim bodyShp As Shape
    Set bodyShp = ws.Shapes.AddShape(msoShapeRectangle, bodyL, bodyT, bodyW, bodyH)
    With bodyShp
        .Fill.Visible = msoFalse
        .Line.Visible = msoTrue
        .Line.ForeColor.RGB = RGB(0, 0, 0)
        .Line.Weight = 1 * PointPerPixel
        .Line.DashStyle = msoLineSolid
        .TextFrame.Characters.text = ""
    End With

    ' --- ƒwƒbƒ_[i“h‚è‚Â‚Ô‚µj ---
    Dim hdrShp As Shape
    Dim fillColor As String
    Set hdrShp = ws.Shapes.AddShape(msoShapeRectangle, hdrL, hdrT, hdrW, hdrH)
    Call ApplySwimlaneHeaderStyle(hdrShp, sw.title, isHoriz, sw)

    ' --- ƒtƒbƒ^[iƒwƒbƒ_[‚Æ“¯‚¶ƒXƒ^ƒCƒ‹j ---
    Dim ftrShp As Shape
    Set ftrShp = ws.Shapes.AddShape(msoShapeRectangle, ftrL, ftrT, ftrW, ftrH)
    Call ApplySwimlaneHeaderStyle(ftrShp, sw.title, isHoriz, sw)

    ' --- 3‚Â‚Ì}Œ`‚ğƒOƒ‹[ƒv‰» ---
    Dim grp As Shape
    Set grp = ws.Shapes.Range(Array(bodyShp.Name, hdrShp.Name, ftrShp.Name)).Group
    sw.groupName = grp.Name
End Sub

' ƒwƒbƒ_[/ƒtƒbƒ^[‹¤’ÊƒXƒ^ƒCƒ‹“K—p
Private Sub ApplySwimlaneHeaderStyle(shp As Shape, title As String, isHoriz As Boolean, sw As SwimlaneData)
    With shp.Fill
        .Visible = msoTrue
        If sw.fillColor = "" Then
            .ForeColor.RGB = RGB(211, 211, 211)  ' ƒ‰ƒCƒgƒOƒŒ[
        Else
            .ForeColor.RGB = HexToRgb(sw.fillColor)
        End If
    End With
    With shp.Line
        .Visible = msoTrue
        .ForeColor.RGB = HexToRgb(sw.outlineColor)
        .Weight = 1 * PointPerPixel
        .DashStyle = msoLineSolid
    End With
    With shp.TextFrame
        .Characters.text = title
        .HorizontalAlignment = xlHAlignCenter
        .VerticalAlignment = xlVAlignCenter
        .HorizontalOverflow = xlOartHorizontalOverflowOverflow
        .VerticalOverflow = xlOartVerticalOverflowOverflow
        .Characters.Font.Color = HexToRgb(sw.textColor)
        .Characters.Font.Size = 11
        If isHoriz Then
            .MarginTop = 0
            .MarginBottom = 0
            .MarginLeft = 7.085 * PointPerPixel
            .MarginRight = 0
        Else
            .MarginTop = 7.0875 * PointPerPixel
            .MarginBottom = 0
            .MarginLeft = 0
            .MarginRight = 0
        End If
    End With
    With shp.TextFrame2
        .WordWrap = msoFalse
        With .TextRange.Characters.ParagraphFormat
            .LineRuleWithin = msoTriStateToggle
            .SpaceWithin = 15.5 * PointPerPixel
        End With
    End With
    
    ' ‰¡Œ^ƒXƒCƒ€ƒŒ[ƒ“: ƒeƒLƒXƒg‚ğ¶90“x‰ñ“]i”½Œv‰ñ‚è = msoTextOrientationUpwardj
    If isHoriz Then
        shp.TextFrame.Orientation = msoTextOrientationUpward
    End If
End Sub

' ============================================================
' •`‰æ: ƒm[ƒhi—v‘fj
' ============================================================

Private Sub DrawNodes(ws As Worksheet, nodes() As NodeData, nCount As Long)
    Dim i As Long
    For i = 0 To nCount - 1
        Call DrawNode(ws, nodes(i))
    Next i
End Sub

' ƒm[ƒh1‚Â‚ğ•`‰æ
Private Sub DrawNode(ws As Worksheet, nd As NodeData)
    Dim shpType As MsoAutoShapeType
    shpType = GetNodeShapeType(nd.nodeType, nd.shapeType)

    ' x, y ‚Í’†SÀ•W‚È‚Ì‚Å¶ãŠp‚É•ÏŠ·
    Dim shp As Shape
    Set shp = ws.Shapes.AddShape(shpType, _
        nd.x - nd.w / 2, nd.y - nd.h / 2, nd.w, nd.h)

    ' “h‚è‚Â‚Ô‚µ
    With shp.Fill
        .Visible = msoTrue
        If nd.status = "active" Then
            .ForeColor.RGB = RGB(255, 250, 205)
        ElseIf nd.status = "inactive" Then
            .ForeColor.RGB = RGB(240, 240, 240)
        Else
            .ForeColor.RGB = HexToRgb(nd.fillColor)
        End If
    End With

    ' ˜gü
    With shp.Line
        If nd.status = "active" Then
            .Visible = msoTrue
            .ForeColor.RGB = RGB(218, 165, 32)
            .Weight = nd.outlineWidth * 1.5
            .DashStyle = msoLineSolid
        ElseIf nd.status = "inactive" Then
            .Visible = msoTrue
            .ForeColor.RGB = RGB(169, 169, 169)
            .Weight = nd.outlineWidth
            .DashStyle = msoLineSolid
        Else
            .Visible = msoTrue
            .ForeColor.RGB = HexToRgb(nd.outlineColor)
            .Weight = nd.outlineWidth
            .DashStyle = msoLineSolid
        End If
    End With

    ' ƒeƒLƒXƒg
    With shp.TextFrame
        .Characters.text = nd.cellText
        .HorizontalAlignment = xlHAlignCenter
        .VerticalAlignment = xlVAlignCenter
        .HorizontalOverflow = xlOartHorizontalOverflowOverflow
        .VerticalOverflow = xlOartVerticalOverflowOverflow
        If nd.status = "active" Then
            .Characters.Font.Color = RGB(218, 165, 32)
        ElseIf nd.status = "inactive" Then
            .Characters.Font.Color = RGB(169, 169, 169)
        Else
            .Characters.Font.Color = HexToRgb(nd.textColor)
        End If
        .MarginTop = 0.83 * nd.fontSize * PointPerPixel      ' 5.67 * PointPerPixel
        .MarginBottom = 0
        .MarginLeft = 0
        .MarginRight = 0
    End With
    
    With shp.TextFrame2
        .WordWrap = msoFalse
        With .TextRange.Characters.ParagraphFormat
            .LineRuleWithin = msoTriStateToggle
            .SpaceWithin = 14 * PointPerPixel
        End With
        With .TextRange.ParagraphFormat
            .LineRuleWithin = msoFalse
            .SpaceWithin = nd.fontSize + 1.5
        End With
        With .TextRange.Font
            .Size = nd.fontSize
            If nd.fontWeight = "bold" Then
                .Bold = msoTrue
            Else
                .Bold = msoFalse
            End If
        End With
    End With
    
    Call SetShapeFont(shp, nd.fontFamily)

    ' ƒGƒbƒWÚ‘±—p‚ÉˆêˆÓ‚Ì–¼‘O‚ğİ’è
    ' shp.Name = "FlowNode_" & CStr(nd.id)
    nd.shapeName = shp.Name

    ' details‚ª‚ ‚éê‡‚ÍAƒm[ƒg‚ğ•`‰æ‚µ‚ÄÚ‘±ü‚ğˆø‚­
    If nd.details <> "" And (nd.note.dx <> 0 Or nd.note.dy <> 0) Then
        Dim noteShpName As String
        noteShpName = DrawNote(ws, nd, nd.note)
        nd.noteShapeName = noteShpName

        Dim noteConnName As String
        noteConnName = DrawLinkToNote(ws, nd)
        nd.noteConnName = noteConnName
    End If
End Sub

' ƒm[ƒhƒ^ƒCƒv‚ÆƒVƒFƒCƒvƒ^ƒCƒv‚©‚çExcelƒVƒFƒCƒví—Ş‚ğ•Ô‚·
Private Function GetNodeShapeType(nodeType As String, shapeType As String) As MsoAutoShapeType
    Select Case LCase(Trim(nodeType))

        Case "terminal", "terminator"
            If LCase(Trim(shapeType)) = "connector" Then
                GetNodeShapeType = msoShapeFlowchartConnector      ' Œ‹‡qi‰~j
            Else
                GetNodeShapeType = msoShapeFlowchartTerminator     ' ’[qiƒXƒ^ƒWƒAƒ€Œ^j
            End If

        Case "process"
            Select Case LCase(Trim(shapeType))
                Case "corner_rounded_rectangle"
                    GetNodeShapeType = msoShapeFlowchartAlternateProcess  ' ‘ã‘Öˆ—
                Case "rounded_rectangle"
                    GetNodeShapeType = msoShapeFlowchartTerminator        ' ’[qiŠÛŠp‹éŒ`j
                Case "ellipse"
                    GetNodeShapeType = msoShapeOval                        ' ‘È‰~
                Case Else  ' "rectangle" ‚Ü‚½‚ÍƒfƒtƒHƒ‹ƒg
                    GetNodeShapeType = msoShapeFlowchartProcess           ' ˆ—i‹éŒ`j
            End Select

        Case "decision"
            GetNodeShapeType = msoShapeFlowchartDecision       ' ”»’fi‚Ğ‚µŒ`j

        Case "io", "i/o"
            GetNodeShapeType = msoShapeFlowchartData           ' ƒf[ƒ^i•½sl•ÓŒ`j

        Case "storage"
            GetNodeShapeType = msoShapeFlowchartMagneticDisk   ' ¥‹CƒfƒBƒXƒNiƒVƒŠƒ“ƒ_j

        Case "document"
            GetNodeShapeType = msoShapeFlowchartDocument       ' ‘—Şi”g’ê‹éŒ`j

        Case Else
            GetNodeShapeType = msoShapeFlowchartProcess        ' ƒtƒH[ƒ‹ƒoƒbƒN
    End Select
End Function

Private Function DrawNote(ws As Worksheet, baseNode As NodeData, note As NoteData)
    Dim noteShp As Shape
    Dim note_with As Double, note_height As Double
    Dim note_x As Double, note_y As Double

    note_with = note.w
    note_height = note.h
    note_x = baseNode.x + note.dx - note_with / 2
    note_y = baseNode.y + note.dy - note_height / 2

    Set noteShp = ws.Shapes.AddShape(msoShapeRectangle, note_x, note_y, note_with, note_height)

    With noteShp.Fill
        .Visible = msoTrue
        .ForeColor.RGB = RGB(255, 249, 204)
    End With
    With noteShp.Line
        .Visible = msoTrue
        .ForeColor.RGB = RGB(214, 185, 77)
        .Weight = 1 * PointPerPixel
        .DashStyle = msoLineSolid
    End With
    With noteShp.TextFrame
        .Characters.text = baseNode.details
        .HorizontalAlignment = xlHAlignLeft
        .VerticalAlignment = xlVAlignTop
        .HorizontalOverflow = xlOartHorizontalOverflowClip
        .VerticalOverflow = xlOartVerticalOverflowEllipsis
        .Characters.Font.Color = RGB(15, 23, 42)
        .Characters.Font.Size = 11 * PointPerPixel
        .MarginTop = 3.78 * PointPerPixel
        .MarginBottom = 0
        .MarginLeft = 3.78 * PointPerPixel
        .MarginRight = 3.78 * PointPerPixel
    End With
    With noteShp.TextFrame2
        .WordWrap = msoTrue
        With .TextRange.Characters.ParagraphFormat
            .LineRuleWithin = msoTriStateToggle
            .SpaceWithin = 12 * PointPerPixel
        End With
    End With

    ' •\¦ó‘Ô‚ª "hidden" ‚Ìê‡‚Íƒm[ƒg‚ğ”ñ•\¦‚É‚·‚é
    If LCase(note.displayState) = "hidden" Then
        noteShp.Visible = msoFalse
    End If

    DrawNote = noteShp.Name
End Function

' ============================================================
' •`‰æ: ƒGƒbƒWiƒŠƒ“ƒNj
' ============================================================

Private Sub DrawEdges(ws As Worksheet, edges() As EdgeData, eCount As Long, _
    nodes() As NodeData, nCount As Long)
    Dim i As Long
    For i = 0 To eCount - 1
        Call DrawEdge(ws, edges(i), nodes, nCount)
    Next i
End Sub

' ƒGƒbƒW1‚Â‚ğ•`‰æ
Private Sub DrawEdge(ws As Worksheet, ed As EdgeData, _
    nodes() As NodeData, nCount As Long)

    ' from/toƒm[ƒh‚ğIDŒŸõ
    Dim fi As Long, ti As Long
    fi = -1: ti = -1
    Dim i As Long
    For i = 0 To nCount - 1
        If nodes(i).id = ed.fromId Then fi = i
        If nodes(i).id = ed.toId Then ti = i
    Next i
    If fi < 0 Or ti < 0 Then Exit Sub   ' ‘Î‰ƒm[ƒh‚ªŒ©‚Â‚©‚ç‚È‚¢

    ' ShapeQÆæ“¾
    Dim fromShp As Shape, toShp As Shape
    On Error Resume Next
    Set fromShp = ws.Shapes(nodes(fi).shapeName)
    Set toShp = ws.Shapes(nodes(ti).shapeName)
    On Error GoTo 0
    If fromShp Is Nothing Or toShp Is Nothing Then Exit Sub

    ' ƒRƒlƒNƒ^í—Ş
    Dim ct As MsoConnectorType
    If LCase(Trim(ed.edgeType)) = "line" Then
        ct = msoConnectorStraight   ' ’¼ü–îˆó
    Else
        ct = msoConnectorElbow      ' ƒJƒMü–îˆóiƒfƒtƒHƒ‹ƒgj
    End If

    ' ƒRƒlƒNƒ^‚ğì¬i‰ŠúˆÊ’u: fromƒm[ƒh’†S ¨ toƒm[ƒh’†Sj
    Dim conn As Shape
    Set conn = ws.Shapes.AddConnector(ct, _
        nodes(fi).x, nodes(fi).y, nodes(ti).x, nodes(ti).y)

    ' Ú‘±“_‚ğİ’è
    Dim fromSite As Long, toSite As Long
    fromSite = GetConnSite(ed.fromCP, fi, ti, nodes)
    toSite = GetConnSite(ed.toCP, ti, fi, nodes)

    conn.ConnectorFormat.BeginConnect fromShp, fromSite
    conn.ConnectorFormat.EndConnect toShp, toSite

    ' xˆÊ’u‚Ü‚½‚ÍyˆÊ’u‚ª“¯‚¶’¼ü‚È‚Ì‚ÉExcel‚Å”­¶‚·‚éƒJƒMü‚Ì”÷–­‚È’i·‚ğ‰ğÁ‚·‚é‘Î‰
    If ct = msoConnectorElbow And conn.height <= 1 Then
        If nodes(fi).x = nodes(ti).x Then
            If nodes(fi).y < nodes(ti).y And ed.fromCP = "bottom" And ed.toCP = "top" Then conn.height = 0
            If nodes(fi).y > nodes(ti).y And ed.fromCP = "top" And ed.toCP = "bottom" Then conn.height = 0
        End If
        If nodes(fi).y = nodes(ti).y Then
            If nodes(fi).x < nodes(ti).x And ed.fromCP = "right" And ed.toCP = "left" Then conn.height = 0
            If nodes(fi).x > nodes(ti).x And ed.fromCP = "left" And ed.toCP = "right" Then conn.height = 0
        End If
    End If
    
    ' ƒGƒbƒW‰ñ‚è‚İİ’è
    If ed.edgeWrapRatio1 <> 0 Then
        conn.Adjustments.Item(1) = ed.edgeWrapRatio1
    End If
    If ed.edgeWrapRatio2 <> 0 Then
        conn.Adjustments.Item(2) = ed.edgeWrapRatio2
    End If

    ' üƒXƒ^ƒCƒ‹
    With conn.Line
        .Weight = ed.lineWidth
        .ForeColor.RGB = HexToRgb(ed.lineColor)
        Select Case LCase(Trim(ed.lineStyle))
            Case "dotted": .DashStyle = msoLineSysDot
            Case "dashed": .DashStyle = msoLineSysDash
            Case Else: .DashStyle = msoLineSolid
        End Select
        Select Case LCase(Trim(ed.arrowKind))
            Case "first":
                .BeginArrowheadStyle = msoArrowheadTriangle
                .EndArrowheadStyle = msoArrowheadNone
            Case "last":
                .BeginArrowheadStyle = msoArrowheadNone
                .EndArrowheadStyle = msoArrowheadTriangle
            Case "both":
                .BeginArrowheadStyle = msoArrowheadTriangle
                .EndArrowheadStyle = msoArrowheadTriangle
            Case Else:
                .BeginArrowheadStyle = msoArrowheadNone
                .EndArrowheadStyle = msoArrowheadNone
        End Select
    End With

    ' ƒ‰ƒxƒ‹•`‰æiw’è‚ª‚ ‚éê‡j
    If Trim(ed.edgeLabel) <> "" Then
        Dim connLabel As Shape
        Dim labelX, labelY, labelW, labelH, adjustX, adjustY As Double
        If ed.labelX > 0 And ed.labelY > 0 Then
            labelW = 100
            labelH = 1
            
            If ed.labelAnchor = "n" Or ed.labelAnchor = "nw" Or ed.labelAnchor = "ne" Then
                adjustY = 2
            ElseIf ed.labelAnchor = "s" Or ed.labelAnchor = "sw" Or ed.labelAnchor = "se" Then
                adjustY = -10 - 3
            Else
                adjustY = -2
            End If

            If ed.labelJustify = "right" Then
                adjustX = -labelW
            ElseIf ed.labelJustify = "left" Then
                adjustX = 0
            Else
                adjustX = -labelW / 2
            End If
                        
            labelX = ed.labelX + adjustX
            labelY = ed.labelY + adjustY
            Set connLabel = ws.Shapes.AddLabel(msoTextOrientationHorizontal, labelX, labelY, labelW, labelH)
        Else
            If ct = msoConnectorStraight Then
                labelX = (nodes(fi).x + nodes(ti).x) / 2 - 75 / 2
                labelY = (nodes(fi).y + nodes(ti).y) / 2 - 20
                labelW = 100
                labelH = 1
                Set connLabel = ws.Shapes.AddLabel(msoTextOrientationHorizontal, labelX, labelY, labelW, labelH)
            Else
                labelX = nodes(fi).x + nodes(fi).w / 2 + 5
                labelY = nodes(fi).y - 20
                labelW = 100
                labelH = 1
                Set connLabel = ws.Shapes.AddLabel(msoTextOrientationHorizontal, labelX, labelY, labelW, labelH)
            End If
        End If

        With connLabel.TextFrame
            .Characters.text = ed.edgeLabel
            If ed.labelJustify = "right" Then
                .HorizontalAlignment = xlHAlignRight
            ElseIf ed.labelJustify = "left" Then
                .HorizontalAlignment = xlHAlignLeft
            Else
                .HorizontalAlignment = xlHAlignCenter
            End If
            .VerticalAlignment = xlVAlignTop
            .HorizontalOverflow = xlOartHorizontalOverflowOverflow
            .VerticalOverflow = xlOartVerticalOverflowOverflow
            .Characters.Font.Color = HexToRgb(ed.textColor)
            .MarginTop = 0
            .MarginBottom = 0
            .MarginLeft = 0
            .MarginRight = 0
            .AutoSize = False
        End With
        With connLabel.TextFrame2
            .WordWrap = msoFalse
            With .TextRange.Characters.ParagraphFormat
                .LineRuleWithin = msoTriStateToggle
                .SpaceWithin = 12.5 * PointPerPixel
            End With
            With .TextRange.Font
                .Size = ed.fontSize
                If ed.fontWeight = "bold" Then
                    .Bold = msoTrue
                Else
                    .Bold = msoFalse
                End If
            End With
        End With
        Call SetShapeFont(connLabel, ed.fontFamily)
    End If
End Sub

' Ú‘±“_•¶š—ñ‚ğExcelƒRƒlƒNƒ^ƒTƒCƒg”Ô†‚É•ÏŠ·
'   ƒTƒCƒg”Ô†: 1=ã, 2=‰E, 3=‰º, 4=¶
'   auto‚Í‘Šèƒm[ƒh‚Æ‚Ì‘Š‘ÎˆÊ’u‚©‚çÅ“K•ûŒü‚ğ©“®‘I‘ğ
Private Function GetConnSite(cpStr As String, nIdx As Long, otherIdx As Long, _
    nodes() As NodeData) As Long
    Dim delta As Double

    Select Case LCase(Trim(cpStr))
        Case "top"
            Select Case LCase(Trim(nodes(nIdx).nodeType))
                Case "io"
                    GetConnSite = 2
                Case "storage"
                    GetConnSite = 2
                Case "terminator"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "connector" Then
                        GetConnSite = 1
                    Else
                        GetConnSite = 1
                    End If
                Case "process"
                     If LCase(Trim(nodes(nIdx).shapeType)) = "ellipse" Then
                        GetConnSite = 1
                    Else
                        GetConnSite = 1
                    End If
                Case Else
                    GetConnSite = 1
                End Select
        Case "right"
            Select Case LCase(Trim(nodes(nIdx).nodeType))
                Case "io"
                    GetConnSite = 6
                Case "storage"
                    GetConnSite = 5
                Case "terminator"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "connector" Then
                        GetConnSite = 7
                    Else
                        GetConnSite = 4
                    End If
                Case "process"
                     If LCase(Trim(nodes(nIdx).shapeType)) = "ellipse" Then
                        GetConnSite = 7
                    Else
                        GetConnSite = 4
                    End If
                Case Else
                    GetConnSite = 4
                End Select
        Case "bottom"
            Select Case LCase(Trim(nodes(nIdx).nodeType))
                Case "io"
                    GetConnSite = 5
                Case "storage"
                    GetConnSite = 4
                Case "terminator"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "connector" Then
                        GetConnSite = 5
                    Else
                        GetConnSite = 3
                    End If
                Case "process"
                     If LCase(Trim(nodes(nIdx).shapeType)) = "ellipse" Then
                        GetConnSite = 5
                    Else
                        GetConnSite = 3
                    End If
                Case Else
                    GetConnSite = 3
                End Select
        Case "left"
            Select Case LCase(Trim(nodes(nIdx).nodeType))
                Case "io"
                    GetConnSite = 3
                Case "storage"
                    GetConnSite = 3
                Case "terminator"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "connector" Then
                        GetConnSite = 3
                    Else
                        GetConnSite = 2
                    End If
                Case "process"
                     If LCase(Trim(nodes(nIdx).shapeType)) = "ellipse" Then
                        GetConnSite = 3
                    Else
                        GetConnSite = 2
                    End If
                Case Else
                    GetConnSite = 2
                End Select
        Case Else
            ' ©“®: ‘Šèƒm[ƒh‚Ì•ûŒüidx/dy ‚Ì‘å‚«‚¢•ûj‚©‚ç”»’è
            Dim dx As Double, dy As Double
            dx = nodes(otherIdx).x - nodes(nIdx).x
            dy = nodes(otherIdx).y - nodes(nIdx).y
            Select Case LCase(Trim(nodes(nIdx).nodeType))
                Case "io"
                    If Abs(dx) >= Abs(dy) Then
                        GetConnSite = IIf(dx >= 0, 6, 3) ' ‰E or ¶  1->2, 2->3, 3->5, 4->6
                    Else
                        GetConnSite = IIf(dy >= 0, 5, 2) ' ‰º or ã
                    End If
                Case "storage"
                    If Abs(dx) >= Abs(dy) Then
                        GetConnSite = IIf(dx >= 0, 5, 3)  ' ‰E or ¶ 1->2, 2->3, 3->4, 4->5
                    Else
                        GetConnSite = IIf(dy >= 0, 4, 2)  ' ‰º or ã
                    End If
                Case "terminator"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "connector" Then
                        If Abs(dx) >= Abs(dy) Then
                            GetConnSite = IIf(dx >= 0, 7, 3)  ' ‰E or ¶ 1->1, 2->3, 3->5, 4->7
                        Else
                            GetConnSite = IIf(dy >= 0, 5, 1)  ' ‰º or ã
                        End If
                    Else
                        If Abs(dx) >= Abs(dy) Then
                            GetConnSite = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
                        Else
                            GetConnSite = IIf(dy >= 0, 3, 1)  ' ‰º or ã
                        End If
                    End If
                Case "process"
                    If LCase(Trim(nodes(nIdx).shapeType)) = "ellipse" Then
                        If dx = 0 Or dy = 0 Then
                            If dx = 0 Then
                                If dy > 0 Then
                                    GetConnSite = 5
                                Else
                                    GetConnSite = 1
                                End If
                            Else
                                If dx > 0 Then
                                    GetConnSite = 7
                                Else
                                    GetConnSite = 3
                                End If
                            End If
                        Else
                            delta = dy / dx
                            If dx > 0 And dy < 0 Then
                                If delta > -0.414 Then
                                    GetConnSite = 7
                                ElseIf delta > -2.414 Then
                                    GetConnSite = 8
                                Else
                                    GetConnSite = 1
                                End If
                            ElseIf dx < 0 And dy < 0 Then
                                If delta > 2.414 Then
                                    GetConnSite = 1
                                ElseIf delta > 0.414 Then
                                    GetConnSite = 2
                                Else
                                    GetConnSite = 3
                                End If
                            ElseIf dx < 0 And dy > 0 Then
                                If delta > -0.414 Then
                                    GetConnSite = 3
                                ElseIf delta > -2.414 Then
                                    GetConnSite = 4
                                Else
                                    GetConnSite = 5
                                End If
                            Else
                                If delta > 2.414 Then
                                    GetConnSite = 5
                                ElseIf delta > 0.414 Then
                                    GetConnSite = 6
                                Else
                                    GetConnSite = 7
                                End If
                            End If
                        End If
                    Else
                        If Abs(dx) >= Abs(dy) Then
                            GetConnSite = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
                        Else
                            GetConnSite = IIf(dy >= 0, 3, 1)  ' ‰º or ã
                        End If
                    End If
                Case Else
                    If Abs(dx) >= Abs(dy) Then
                        GetConnSite = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
                    Else
                        GetConnSite = IIf(dy >= 0, 3, 1)  ' ‰º or ã
                    End If
            End Select
    End Select
End Function

' ============================================================
' •`‰æ: Node‚©‚çNote‚Ö‚Ì’¼üƒŠƒ“ƒN
' ============================================================

Private Function DrawLinkToNote(ws As Worksheet, baseNode As NodeData)

    Dim note As NoteData
    note = baseNode.note

    If baseNode.shapeName = "" Or baseNode.noteShapeName = "" Then
        DrawLinkToNote = ""
        Exit Function
    End If

    ' ShapeQÆæ“¾
    Dim fromShp As Shape, toShp As Shape
    On Error Resume Next
    Set fromShp = ws.Shapes(baseNode.shapeName)
    Set toShp = ws.Shapes(baseNode.noteShapeName)
    On Error GoTo 0
    If fromShp Is Nothing Or toShp Is Nothing Then
        DrawLinkToNote = ""
        Exit Function
    End If

    ' ƒRƒlƒNƒ^í—Ş
    Dim ct As MsoConnectorType
    ct = msoConnectorStraight   ' ’¼ü–îˆó

    ' ƒRƒlƒNƒ^‚ğì¬i‰ŠúˆÊ’u: fromƒm[ƒh’†S ¨ toƒm[ƒh’†Sj
    Dim conn As Shape
    Set conn = ws.Shapes.AddConnector(ct, _
        baseNode.x, baseNode.y, baseNode.x + note.dx, baseNode.y + note.dy)

    ' Ú‘±“_‚ğİ’è
    Dim fromSite As Long, toSite As Long
    fromSite = GetConnSiteOfNodeToNote(baseNode)
    toSite = GetConnSiteOfNoteFromNode(baseNode)

    conn.ConnectorFormat.BeginConnect fromShp, fromSite
    conn.ConnectorFormat.EndConnect toShp, toSite
    
    ' üƒXƒ^ƒCƒ‹i‘¾‚³ 1ptA–îˆó‚È‚µj
    With conn.Line
        .Weight = 1 * PointPerPixel
        .ForeColor.RGB = RGB(214, 185, 77)
        .DashStyle = msoLineSolid
        .BeginArrowheadStyle = msoArrowheadNone
        .EndArrowheadStyle = msoArrowheadNone
    End With

    DrawLinkToNote = conn.Name
 End Function

Private Function GetConnSiteOfNodeToNote(baseNode As NodeData) As Long
    Dim note As NoteData
    note = baseNode.note

    ' ©“®: ‘Šèƒm[ƒh‚Ì•ûŒüidx/dy ‚Ì‘å‚«‚¢•ûj‚©‚ç”»’è
    Dim dx As Double, dy As Double
    dx = note.dx
    dy = note.dy
    Dim delta As Double

    Dim nodeType As String, nodeShapeType As String, noteType As String, noteShapeType As String
    nodeType = baseNode.nodeType
    nodeShapeType = baseNode.shapeType
    noteType = "note"
    noteShapeType = "rectangle" ' ƒm[ƒg‚Íí‚É‹éŒ`

    Select Case LCase(nodeType)
        Case "io"
            If Abs(dx) >= Abs(dy) Then
                GetConnSiteOfNodeToNote = IIf(dx >= 0, 6, 3) ' ‰E or ¶  1->2, 2->3, 3->5, 4->6
            Else
                GetConnSiteOfNodeToNote = IIf(dy >= 0, 5, 2) ' ‰º or ã
            End If
        Case "storage"
            If Abs(dx) >= Abs(dy) Then
                GetConnSiteOfNodeToNote = IIf(dx >= 0, 5, 3)  ' ‰E or ¶ 1->2, 2->3, 3->4, 4->5
            Else
                GetConnSiteOfNodeToNote = IIf(dy >= 0, 4, 2)  ' ‰º or ã
            End If
        Case "terminator"
            If LCase(nodeShapeType) = "connector" Then
                If Abs(dx) >= Abs(dy) Then
                    GetConnSiteOfNodeToNote = IIf(dx >= 0, 7, 3)  ' ‰E or ¶ 1->1, 2->3, 3->5, 4->7
                Else
                    GetConnSiteOfNodeToNote = IIf(dy >= 0, 5, 1)  ' ‰º or ã
                End If
            Else
                If Abs(dx) >= Abs(dy) Then
                    GetConnSiteOfNodeToNote = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
                Else
                    GetConnSiteOfNodeToNote = IIf(dy >= 0, 3, 1)  ' ‰º or ã
                End If
            End If
        Case "process"
            If LCase(nodeShapeType) = "ellipse" Then
                If dx = 0 Or dy = 0 Then
                    If dx = 0 Then
                        If dy > 0 Then
                            GetConnSiteOfNodeToNote = 5
                        Else
                            GetConnSiteOfNodeToNote = 1
                        End If
                    Else
                        If dx > 0 Then
                            GetConnSiteOfNodeToNote = 7
                        Else
                            GetConnSiteOfNodeToNote = 3
                        End If
                    End If
                Else
                    delta = dy / dx
                    If dx > 0 And dy < 0 Then
                        If delta > -0.414 Then
                            GetConnSiteOfNodeToNote = 7
                        ElseIf delta > -2.414 Then
                            GetConnSiteOfNodeToNote = 8
                        Else
                            GetConnSiteOfNodeToNote = 1
                        End If
                    ElseIf dx < 0 And dy < 0 Then
                        If delta > 2.414 Then
                            GetConnSiteOfNodeToNote = 1
                        ElseIf delta > 0.414 Then
                            GetConnSiteOfNodeToNote = 2
                        Else
                            GetConnSiteOfNodeToNote = 3
                        End If
                    ElseIf dx < 0 And dy > 0 Then
                        If delta > -0.414 Then
                            GetConnSiteOfNodeToNote = 3
                        ElseIf delta > -2.414 Then
                            GetConnSiteOfNodeToNote = 4
                        Else
                            GetConnSiteOfNodeToNote = 5
                        End If
                    Else
                        If delta > 2.414 Then
                            GetConnSiteOfNodeToNote = 5
                        ElseIf delta > 0.414 Then
                            GetConnSiteOfNodeToNote = 6
                        Else
                            GetConnSiteOfNodeToNote = 7
                        End If
                    End If
                End If
            Else
                If Abs(dx) >= Abs(dy) Then
                    GetConnSiteOfNodeToNote = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
                Else
                    GetConnSiteOfNodeToNote = IIf(dy >= 0, 3, 1)  ' ‰º or ã
                End If
            End If
        Case Else
            If Abs(dx) >= Abs(dy) Then
                GetConnSiteOfNodeToNote = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
            Else
                GetConnSiteOfNodeToNote = IIf(dy >= 0, 3, 1)  ' ‰º or ã
            End If
    End Select
End Function

Private Function GetConnSiteOfNoteFromNode(baseNode As NodeData) As Long
    Dim note As NoteData
    note = baseNode.note

    ' ©“®: ‘Šèƒm[ƒh‚Ì•ûŒüidx/dy ‚Ì‘å‚«‚¢•ûj‚©‚ç”»’è
    Dim dx As Double, dy As Double
    dx = -note.dx
    dy = -note.dy

    If Abs(dx) >= Abs(dy) Then
        GetConnSiteOfNoteFromNode = IIf(dx >= 0, 4, 2)  ' ‰E or ¶
    Else
        GetConnSiteOfNoteFromNode = IIf(dy >= 0, 3, 1)  ' ‰º or ã
    End If

End Function

' ============================================================
' Z-order ’²®
' ============================================================

' •`‰æ—Dæ‡ˆÊi‘O–Ê‚©‚çj: ƒm[ƒh > ƒGƒbƒW > ƒXƒCƒ€ƒŒ[ƒ“
' ƒXƒCƒ€ƒŒ[ƒ“ƒOƒ‹[ƒv‚ğÅ”w–ÊAƒm[ƒh‚ğÅ‘O–Ê‚ÉˆÚ“®‚·‚é
Private Sub AdjustZOrder(ws As Worksheet, nodes() As NodeData, nCount As Long, _
    swimlanes() As SwimlaneData, sCount As Long)

    Dim i   As Long
    Dim shp, conn As Shape

    ' 1. ƒXƒCƒ€ƒŒ[ƒ“ƒOƒ‹[ƒv‚ğÅ”w–Ê‚Ö‘—‚é
    For i = 0 To sCount - 1
        If swimlanes(i).groupName <> "" Then
            Set shp = Nothing
            On Error Resume Next
            Set shp = ws.Shapes(swimlanes(i).groupName)
            On Error GoTo 0
            If Not shp Is Nothing Then shp.ZOrder msoSendToBack
        End If
    Next i

    ' 2. ƒm[ƒh‚ğÅ‘O–Ê‚Ö‚Á‚Ä‚­‚é
    For i = 0 To nCount - 1
        If nodes(i).shapeName <> "" Then
            Set shp = Nothing
            On Error Resume Next
            Set shp = ws.Shapes(nodes(i).shapeName)
            On Error GoTo 0
            If Not shp Is Nothing Then shp.ZOrder msoBringToFront
        End If
    Next i

    ' 3. ƒm[ƒg‚Æƒm[ƒg‚Ö‚ÌƒŠƒ“ƒN‚ğÅ‘O–Ê‚Ö‚Á‚Ä‚­‚é
    For i = 0 To nCount - 1
        If nodes(i).noteShapeName <> "" Then
            Set shp = Nothing
            On Error Resume Next
            Set shp = ws.Shapes(nodes(i).noteShapeName)
            Set conn = ws.Shapes(nodes(i).noteConnName)
            On Error GoTo 0
            If Not shp Is Nothing Then shp.ZOrder msoBringToFront
            If Not conn Is Nothing Then conn.ZOrder msoBringToFront
        End If
    Next i

End Sub

' ============================================================
' ƒ†[ƒeƒBƒŠƒeƒB
' ============================================================

' "#rrggbb" Œ`®‚ÌF•¶š—ñ‚ğExcel RGB’l‚É•ÏŠ·
Private Function HexToRgb(hexColor As String) As Long
    Dim s As String
    s = Trim(Replace(hexColor, "#", ""))

    If Len(s) < 6 Then
        HexToRgb = RGB(255, 255, 255)  ' ƒfƒtƒHƒ‹ƒg: ”’
        Exit Function
    End If

    HexToRgb = RGB(CLng("&H" & Mid(s, 1, 2)), _
                   CLng("&H" & Mid(s, 3, 2)), _
                   CLng("&H" & Mid(s, 5, 2)))
End Function


' ================================
' ƒtƒ@ƒCƒ‹ƒ_ƒCƒAƒƒO‚ÅJSONƒtƒ@ƒCƒ‹ƒpƒX‚ğæ“¾(macOS—p)
' –ß‚è’l‚Í‘I‘ğ‚µ‚½ƒtƒ@ƒCƒ‹–¼‚ğŠÜ‚Şƒtƒ@ƒCƒ‹ƒpƒX(String)
' ================================
Private Function GetJsonFilePathForMacOS() As String
    GetJsonFilePathForMacOS = Application.GetOpenFilename(title:="Select a JSON File")
End Function


' ================================
' macOS—pUTF-8ƒtƒ@ƒCƒ‹“ÇiAppleScriptg—pAÀs•s‰Â‚È‚ç’Êí“Ç‚İ‚İ‚ğ‚İ‚é)
' –ß‚è’l‚ÍVBA‚ÌUnicode•¶š—ñ(String)
' ================================
Function ReadUTF8FileForMacOS(ByVal filePath As String) As String

    ' macOS—pƒtƒ@ƒCƒ‹“Ç‚İ‚İˆ—
    On Error GoTo Fallback

    ReadUTF8FileForMacOS = AppleScriptTask( _
        "ReadTextFile.scpt", _
        "readTextFile", _
        filePath)

    Debug.Print ReadUTF8FileForMacOS

    Exit Function

Fallback:

    ' AppleScriptTask‚ªÀs‚Å‚«‚È‚¢ê‡‚Ì‘ã‘Öˆ—
    Err.Clear
    On Error GoTo 0

    ReadUTF8FileForMacOS = ReadUtf8TextFile(filePath)

End Function

' ================================
' UTF-8ƒeƒLƒXƒgƒtƒ@ƒCƒ‹“Ç
' –ß‚è’l‚ÍVBA‚ÌUnicode•¶š—ñ(String)
' ================================
Function ReadUtf8TextFile(ByVal filePath As String) As String
    Dim fileNo As Integer
    Dim fileSize As Long
    Dim bytes() As Byte
    Dim text As String
    
    fileNo = FreeFile
    
    ' ƒoƒCƒiƒŠ‚ÅŠJ‚­
    Open filePath For Binary Access Read As #fileNo
    
    fileSize = LOF(fileNo)
    If fileSize <= 0 Then
        Close #fileNo
        ReadUtf8TextFile = ""
        Exit Function
    End If
    
    ReDim bytes(0 To fileSize - 1) As Byte
    Get #fileNo, , bytes
    Close #fileNo
    
    ' UTF-8 BOM ‚ª‚ ‚ê‚Îœ‹
    If fileSize >= 3 Then
        If bytes(0) = &HEF And bytes(1) = &HBB And bytes(2) = &HBF Then
            text = Utf8BytesToString(bytes, 3)
        Else
            text = Utf8BytesToString(bytes, 0)
        End If
    Else
        text = Utf8BytesToString(bytes, 0)
    End If
    
    ReadUtf8TextFile = text
End Function


' ================================
' UTF-8ƒoƒCƒg”z—ñ ¨ VBA•¶š—ñ(Unicode)
' startPos ‚Åæ“ªƒIƒtƒZƒbƒgw’è‰Â”\
' ================================
Function Utf8BytesToString(ByRef bytes() As Byte, Optional ByVal startPos As Long = 0) As String
    Dim i As Long
    Dim b1 As Long, b2 As Long, b3 As Long, b4 As Long
    Dim codePoint As Long
    Dim result As String
    
    result = ""
    i = startPos
    
    Do While i <= UBound(bytes)
        b1 = bytes(i)
        
        Select Case True
            ' 1ƒoƒCƒgASCII
            Case b1 < &H80
                result = result & ChrW(b1)
                i = i + 1
            
            ' 2ƒoƒCƒgUTF-8
            Case (b1 And &HE0) = &HC0
                If i + 1 > UBound(bytes) Then Exit Do
                b2 = bytes(i + 1)
                codePoint = ((b1 And &H1F) * &H40) Or (b2 And &H3F)
                result = result & ChrW(codePoint)
                i = i + 2
            
            ' 3ƒoƒCƒgUTF-8
            Case (b1 And &HF0) = &HE0
                If i + 2 > UBound(bytes) Then Exit Do
                b2 = bytes(i + 1)
                b3 = bytes(i + 2)
                codePoint = ((b1 And &HF) * &H1000) Or _
                            ((b2 And &H3F) * &H40) Or _
                            (b3 And &H3F)
                result = result & ChrW(codePoint)
                i = i + 3
            
            ' 4ƒoƒCƒgUTF-8
            Case (b1 And &HF8) = &HF0
                If i + 3 > UBound(bytes) Then Exit Do
                b2 = bytes(i + 1)
                b3 = bytes(i + 2)
                b4 = bytes(i + 3)
                
                codePoint = ((b1 And &H7) * &H40000) Or _
                            ((b2 And &H3F) * &H1000) Or _
                            ((b3 And &H3F) * &H40) Or _
                            (b4 And &H3F)
                
                ' UTF-16ƒTƒƒQ[ƒgƒyƒA‚É•ÏŠ·
                codePoint = codePoint - &H10000
                result = result & ChrW((&HD800 Or ((codePoint \ &H400) And &H3FF)))
                result = result & ChrW((&HDC00 Or (codePoint And &H3FF)))
                i = i + 4
            
            Case Else
                ' •s³ƒoƒCƒg—ñ‚Í’uŠ·•¶š‘Š“–‚É‚·‚é
                result = result & "?"
                i = i + 1
        End Select
    Loop
    
    Utf8BytesToString = result
End Function

Public Sub SetShapeFont( _
    ByVal shp As Shape, _
    ByVal fontName As String)

    Dim latinFont As String
    Dim japaneseFont As String

    Select Case LCase(Trim(fontName))

        Case "arial"

            latinFont = "Arial"

#If Mac Then
            japaneseFont = "Hiragino Sans"
#Else
            japaneseFont = "Meiryo"
#End If

        Case "courier", "courier new"

            latinFont = "Courier New"

#If Mac Then
            japaneseFont = "Osaka-Mono"
#Else
            japaneseFont = "MS Gothic"
#End If

        Case "helvetica"

#If Mac Then
            latinFont = "Helvetica"
            japaneseFont = "Hiragino Sans"
#Else
            latinFont = "Arial"
            japaneseFont = "Yu Gothic"
#End If

        Case "times", "times new roman"

            latinFont = "Times New Roman"

#If Mac Then
            japaneseFont = "Hiragino Mincho ProN"
#Else
            japaneseFont = "Yu Mincho"
#End If

        Case Else

            latinFont = fontName
            japaneseFont = fontName

    End Select

    ' }Œ`‚ÌƒtƒHƒ“ƒgİ’è
    With shp.TextFrame2.TextRange.Font

        .Name = latinFont
        .NameFarEast = japaneseFont

    End With

End Sub

Public Function IsGroupableShape(ByVal shp As Shape) As Boolean

    Select Case shp.Type

        Case msoAutoShape, _
             msoCallout, _
             msoFreeform, _
             msoGroup, _
             msoLine, _
             msoLinkedPicture, _
             msoPicture, _
             msoTextEffect, _
             msoTextBox

            IsGroupableShape = True

        Case Else

            IsGroupableShape = False

    End Select

End Function

Private Sub GroupAllGroupableShapes()

    Dim ws As Worksheet
    Dim shp As Shape
    Dim grp As Shape
    Dim shapeNames() As Variant
    Dim cnt As Long

    Set ws = ActiveSheet

    cnt = 0

    ' ƒOƒ‹[ƒv‰»‘ÎÛ‚Ì}Œ`–¼‚ğæ“¾
    For Each shp In ws.Shapes

        If IsGroupableShape(shp) Then

            ReDim Preserve shapeNames(0 To cnt)
            shapeNames(cnt) = shp.Name
            cnt = cnt + 1

        Else

            Debug.Print "‘ÎÛŠO: " & shp.Name

        End If

    Next shp

    ' ‘ÎÛ}Œ`‚ª‘¶İ‚µ‚È‚¢ê‡
    If cnt = 0 Then Exit Sub

    On Error GoTo ErrorHandler

    ' ƒOƒ‹[ƒv‰»
    If cnt = 1 Then
        Set grp = ws.Shapes(shapeNames(0))
    Else
        Set grp = ws.Shapes.Range(shapeNames).Group
    End If

    ' ƒOƒ‹[ƒv‚ÌƒvƒƒpƒeƒB‚ğİ’è
    With grp

        .Name = "FlowchartGroup"

        ' ƒZƒ‹‚É‡‚í‚¹‚ÄˆÚ“®‚·‚é‚ªƒTƒCƒY•ÏX‚Í‚µ‚È‚¢
        .Placement = xlMove

    End With

    Exit Sub

ErrorHandler:

    MsgBox "An error occurred. / ƒGƒ‰[‚ª”­¶‚µ‚Ü‚µ‚½B: " & Err.Description, vbExclamation

End Sub

Private Function CountGroupableShapes()

    Dim ws As Worksheet
    Dim shp As Shape
    Dim grp As Shape
    Dim shapeNames() As Variant
    Dim cnt As Long

    Set ws = ActiveSheet

    cnt = 0

    ' ƒOƒ‹[ƒv‰»‘ÎÛ‚Ì}Œ`–¼‚ğæ“¾
    For Each shp In ws.Shapes

        If IsGroupableShape(shp) Then

            ReDim Preserve shapeNames(0 To cnt)
            shapeNames(cnt) = shp.Name
            cnt = cnt + 1

        Else

            Debug.Print "‘ÎÛŠO: " & shp.Name

        End If

    Next shp

    CountGroupableShapes = cnt

End Function
