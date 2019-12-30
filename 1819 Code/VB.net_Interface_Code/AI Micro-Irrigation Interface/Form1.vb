Imports System
Imports System.IO.Ports
Imports System.Data.Odbc

Public Class Form1
    Dim WithEvents Port As SerialPort =
    New SerialPort("COM5", 9600, Parity.None, 8, StopBits.One)
    Dim messagereturn As String
    Dim messagereturn2() As String
    Dim HealthArray = New Integer() {1, 3, 1, 3, 0, 0, 0, 1, 3, 1, 0, 1}
    Dim ColorArray = New Integer() {18, 21, 20, 25, 0, 0, 0, 18, 19, 17, 0, 18}
    Dim AverageWaterArray = New Double() {6.13, 5.94, 6.38, 5.92, 6.01, 6.14, 6.1, 6.07, 5.93, 5.89, 6.01, 5.96}
    Dim ColorRangeArray = New Integer() {60, 150, 0, 40, 40, 60}
    Dim MinIndex = 0
    Dim MaxIndex = 1
    Public PlantWaterData As New List(Of Double)
    Public PlantColorData As New List(Of Integer)
    Public PlantDateData As New List(Of DateTime)
    Dim currentPlant As Integer
    Dim ObjCon As OdbcConnection
    Dim ObjCommand As OdbcCommand
    Dim Sent As Boolean = False
    Dim arrImage() As Byte
    Dim printString As String
    Public PlantNumberPass As Integer
    Dim ColorDataPass As New List(Of Integer)
    Dim WaterDataPass As New List(Of Integer)
    Dim MinimumColor As Integer
    Dim Percentage As Double = 0
    Dim PlantArea As Double
    Dim TempDistance As Double

    'When Program First Opens
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load 'when form is first loaded/launched

        'Open communication with database
        OpenDB()

        'Initialize Webcam
        ClearAllObject()
        CaptureImage()

        'Make labels invisible temporarily
        PlantLabel.Visible = False
        ColorLabel.Visible = False
        HealthLabel.Visible = False
        HealthComboBox.Visible = False
        ColorTextBox.Visible = False
        UpdateLabel.Visible = False

        'Use data to populate plant arrays
        For x = 0 To 11
            SetLabels(x)
            If x = 0 Then
                ChangeColors(ColorArray(0), Plant1)
            ElseIf x = 1 Then
                ChangeColors(ColorArray(1), Plant2)
            ElseIf x = 2 Then
                ChangeColors(ColorArray(2), Plant3)
            ElseIf x = 3 Then
                ChangeColors(ColorArray(3), Plant4)
            ElseIf x = 4 Then
                ChangeColors(ColorArray(4), Plant5)
            ElseIf x = 5 Then
                ChangeColors(ColorArray(5), Plant6)
            ElseIf x = 6 Then
                ChangeColors(ColorArray(6), Plant7)
            ElseIf x = 7 Then
                ChangeColors(ColorArray(7), Plant8)
            ElseIf x = 8 Then
                ChangeColors(ColorArray(8), Plant9)
            ElseIf x = 9 Then
                ChangeColors(ColorArray(9), Plant10)
            ElseIf x = 10 Then
                ChangeColors(ColorArray(10), Plant11)
            Else
                ChangeColors(ColorArray(11), Plant12)
            End If
        Next

        'Open Com Port
        AddHandler Port.DataReceived, New SerialDataReceivedEventHandler(AddressOf port_DataReceived)
        Port.Open()
    End Sub

    'Used to Initialize Webcam
    Private Sub ClearAllObject()
        On Error Resume Next

        pView.BackColor = Color.Black
        pView.BackgroundImageLayout = ImageLayout.Stretch
        pView.Image = Nothing
        pView.SizeMode = PictureBoxSizeMode.StretchImage
        pView.Refresh()

    End Sub

    'Open communication with database
    Public Sub OpenDB(Optional ByRef l_DoNotLog As Object = Nothing)
        Dim StrCn As String = ""
        Dim ConnectTry As Short
        Dim DBConnect As Boolean
        Dim l_CurrTime As Date
        Dim l_ErrNumber As Integer

        'Try to connect if not give error
        Try
            DBConnect = False : ConnectTry = 0
            StrCn = "User ID=root; Password=arya123;Host=127.0.0.1;Port=3306;DSN=AI;Database=plant_data"
            ObjCon = New Odbc.OdbcConnection
            With ObjCon
                .ConnectionString = StrCn
                While (Not (DBConnect)) And (ConnectTry < 5)
                    l_CurrTime = DateAdd(Microsoft.VisualBasic.DateInterval.Second, 10, Now)
                    .Open()
                    l_ErrNumber = Err.Number
                    If l_ErrNumber <> 0 Then
                        ConnectTry = ConnectTry + 1
                        While l_CurrTime < Now
                            System.Windows.Forms.Application.DoEvents()
                        End While
                    Else
                        DBConnect = True
                    End If
                End While
            End With

            If Not DBConnect Then
                MsgBox("Please check Database Connectivity. String Used: " & StrCn & vbNewLine & "ERROR [" & Err.Number & ": " & Err.Description & "]", MsgBoxStyle.Critical, "Aborting " & My.Application.Info.Title)
                End
            End If
        Catch ex As Exception
            MsgBox("Please check Database Connectivity. DSN : " & StrCn & "  Required  " & vbNewLine & "ERROR [" & Err.Number & ": " & Err.Description & "]", MsgBoxStyle.Critical, "Aborting " & My.Application.Info.Title)
            End
        End Try
    End Sub

    'Read output from database
    Public Function CnExecuteReader(ByVal SQL As String) As OdbcDataReader
        Dim ObjDataReader As OdbcDataReader
        Try
            ObjCommand = New OdbcCommand(SQL, ObjCon)
            ObjDataReader = ObjCommand.ExecuteReader

            Return ObjDataReader
        Catch ex As Exception
        End Try
    End Function

    'Send information to database
    Public Function CnExecute(ByRef StrSQL As String) As Integer
        On Error GoTo CnExecute_ERROR
        Dim RecAffect As Integer
        Dim ObjCmd As Odbc.OdbcCommand

        ObjCmd = New Odbc.OdbcCommand(StrSQL, ObjCon)
        RecAffect = ObjCmd.ExecuteScalar()
        CnExecute = Val(RecAffect)
        If Err.Number = 0 Then
        Else
            Err.Clear()
        End If
CnExecute_EXIT:
        Exit Function
CnExecute_ERROR:
        Err.Clear()
        GoTo CnExecute_EXIT
    End Function

    'Calculates average color change/mL of water added (AI Implementation using Dynamic Linear Regression)
    Private Function CalculateAverage(plantNumber As Integer, newColor As Integer, newWater As Integer, n As Integer)
        Dim ObjReader As OdbcDataReader

        'Search for all data from database
        Dim StrSQL = "select * from plant_water_details where plant_number="
        StrSQL += plantNumber
        StrSQL += ";"

        'Collect all data from database
        While ObjReader.Read
            Dim number = ObjReader.Item("plant_number")
            Dim water = ObjReader.Item("water_volume")
            Dim color = ObjReader.Item("color")
            Dim time = ObjReader.Item("date_time_collected")
            ColorDataPass.Add(color)
            WaterDataPass.Add(water)
        End While
        ObjReader.Close()
        ObjReader = Nothing
        ColorDataPass.Add(newColor)
        WaterDataPass.Add(newWater)

        'Define variables used in dynamic linear regression function
        Dim sumx As Long = 0
        Dim sumy As Long = 0
        Dim sumxy As Long = 0
        Dim sumxsquared As Long = 0
        Dim slope As Double = 0
        Dim yint As Double = 0

        'Populate variables with data from entire data set
        For x = 0 To n + 1
            sumx += WaterDataPass(x)
            sumy += ColorDataPass(x)
            sumxy += (WaterDataPass(x) * ColorDataPass(x))
            sumxsquared += (WaterDataPass(x) * WaterDataPass(x))
        Next
        Return (((n * sumxy) - (sumx * sumy)) / ((n * sumxsquared) - (sumx * sumx)))
    End Function

    'Initialize Camera
    Private Sub CaptureImage()
        On Error Resume Next
        'Set up connection with webcam
        Dim strName As String = Space(100)
        Dim strVer As String = Space(100)
        Dim bReturn As Boolean
        Dim x As Integer = 0
        Dim y = capGetDriverDescriptionA(x, strName, 100, strVer, 100)
        iDevice = 0

        'Load And Capture Device
        OpenPreviewWindow()
    End Sub

    'Save image from webcam to files
    Private Sub ImageSave()
        On Error Resume Next

        Dim data As IDataObject
        Dim bmap As Image

        'Copy image to clipboard
        SendMessage(hHwnd, WM_CAP_EDIT_COPY, 0, 0)

        'Get image from clipboard, convert it to a bitmap, and save it to files
        data = Clipboard.GetDataObject()
        If data.GetDataPresent(GetType(System.Drawing.Bitmap)) Then
            bmap = CType(data.GetData(GetType(System.Drawing.Bitmap)), Image)
            pView.Image = bmap
            bmap.Save("C:\Users\Arya\Desktop\Research Project Arduino Code\colorsummarizer\img\tucan.jpg", Imaging.ImageFormat.Jpeg)

        End If

        data = Nothing
    End Sub

    'Open live feed of webcam
    Private Sub OpenPreviewWindow()
        On Error Resume Next

        Dim iHeight As Integer = pView.Height
        Dim iWidth As Integer = pView.Width

        'Open Preview window in picturebox
        hHwnd = capCreateCaptureWindowA(iDevice, WS_VISIBLE Or WS_CHILD, 0, 0, 640, 480, pView.Handle.ToInt32, 0)

        'Connect to device
        If SendMessage(hHwnd, WM_CAP_DRIVER_CONNECT, iDevice, 0) Then

            'Set the preview scale
            SendMessage(hHwnd, WM_CAP_SET_SCALE, True, 0)

            'Set the preview rate in milliseconds
            SendMessage(hHwnd, WM_CAP_SET_PREVIEWRATE, 66, 0)

            'Start previewing the image from the camera
            SendMessage(hHwnd, WM_CAP_SET_PREVIEW, True, 0)

            'Resize window to fit in picturebox
            SetWindowPos(hHwnd, HWND_BOTTOM, 0, 0, pView.Width, pView.Height,
                    SWP_NOMOVE Or SWP_NOZORDER)
        Else
            'Error connecting to device close window
            DestroyWindow(hHwnd)

            pView.Image = Nothing
            pView.SizeMode = PictureBoxSizeMode.StretchImage
            pView.BackColor = Color.Black
            pView.BackgroundImage = Nothing
            pView.BackgroundImageLayout = ImageLayout.None
            pView.Refresh()
        End If
    End Sub

    'Close live feed of webcam
    Private Sub ClosePreviewWindow()
        On Error Resume Next

        'Disconnect from device
        SendMessage(hHwnd, WM_CAP_DRIVER_DISCONNECT, iDevice, 0)

        'Close window
        DestroyWindow(hHwnd)

        pView.Image = Nothing
        pView.SizeMode = PictureBoxSizeMode.StretchImage
        pView.BackColor = Color.Black
        pView.BackgroundImage = Nothing
        pView.BackgroundImageLayout = ImageLayout.None
        pView.Refresh()

    End Sub

    'Analyze image from webcam and extract color and pixel %
    Private Function GetColor()
        'Save current image
        ImageSave()

        Dim returnArray(6) As Double

        'Use color summarizer (command prompt tool) to analyze image
        Dim oProcess2 As New Process()
        Dim oStartInfo2 As New ProcessStartInfo("""C:\Users\Arya\Desktop\Research Project Arduino Code\colorsummarizer\bin\colorsummarizer.exe""", "-image ""C:\Users\Arya\Desktop\Research Project Arduino Code\colorsummarizer\img\tucan.jpg"" -clusters 7")
        oStartInfo2.RedirectStandardOutput = True
        oStartInfo2.RedirectStandardError = True
        oStartInfo2.CreateNoWindow = True
        oStartInfo2.WindowStyle = ProcessWindowStyle.Hidden
        oStartInfo2.UseShellExecute = False
        oProcess2.StartInfo = oStartInfo2
        oProcess2.Start()

        'Read output
        Dim sOutput2 As String
        Using oStreamReader As System.IO.StreamReader = oProcess2.StandardOutput
            sOutput2 = oStreamReader.ReadToEnd()
        End Using
        Console.WriteLine(sOutput2)
        Dim breakArray = sOutput2.Split(" ")

        'Check to see which cluster is desired color and return the values
        If Convert.ToInt16(breakArray(32)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(32)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(33)) > 12 And Convert.ToInt16(breakArray(34)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(32))
            returnArray(1) = Convert.ToInt16(breakArray(33))
            returnArray(2) = Convert.ToInt16(breakArray(34))
            returnArray(3) = Convert.ToDouble(breakArray(24))
            returnArray(4) = Convert.ToDouble(breakArray(26))
            returnArray(5) = Convert.ToDouble(breakArray(27))
            returnArray(6) = Convert.ToDouble(breakArray(28))
            Return returnArray
        ElseIf Convert.ToInt16(breakArray(71)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(71)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(72)) > 12 And Convert.ToInt16(breakArray(73)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(71))
            returnArray(1) = Convert.ToInt16(breakArray(72))
            returnArray(2) = Convert.ToInt16(breakArray(73))
            returnArray(3) = Convert.ToDouble(breakArray(63))
            returnArray(4) = Convert.ToDouble(breakArray(65))
            returnArray(5) = Convert.ToDouble(breakArray(66))
            returnArray(6) = Convert.ToDouble(breakArray(67))
            Return returnArray
        ElseIf Convert.ToInt16(breakArray(110)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(110)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(111)) > 12 And Convert.ToInt16(breakArray(112)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(110))
            returnArray(1) = Convert.ToInt16(breakArray(111))
            returnArray(2) = Convert.ToInt16(breakArray(112))
            returnArray(3) = Convert.ToDouble(breakArray(102))
            returnArray(4) = Convert.ToDouble(breakArray(104))
            returnArray(5) = Convert.ToDouble(breakArray(105))
            returnArray(6) = Convert.ToDouble(breakArray(106))

            Return returnArray
        ElseIf Convert.ToInt16(breakArray(149)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(149)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(150)) > 12 And Convert.ToInt16(breakArray(151)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(149))
            returnArray(1) = Convert.ToInt16(breakArray(150))
            returnArray(2) = Convert.ToInt16(breakArray(151))
            returnArray(3) = Convert.ToDouble(breakArray(141))
            returnArray(4) = Convert.ToDouble(breakArray(143))
            returnArray(5) = Convert.ToDouble(breakArray(144))
            returnArray(6) = Convert.ToDouble(breakArray(145))
            Return returnArray
        ElseIf Convert.ToInt16(breakArray(188)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(188)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(189)) > 12 And Convert.ToInt16(breakArray(190)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(188))
            returnArray(1) = Convert.ToInt16(breakArray(189))
            returnArray(2) = Convert.ToInt16(breakArray(190))
            returnArray(3) = Convert.ToDouble(breakArray(180))
            returnArray(4) = Convert.ToDouble(breakArray(182))
            returnArray(5) = Convert.ToDouble(breakArray(183))
            returnArray(6) = Convert.ToDouble(breakArray(184))
            Return returnArray
        ElseIf Convert.ToInt16(breakArray(227)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(227)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(228)) > 12 And Convert.ToInt16(breakArray(229)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(227))
            returnArray(1) = Convert.ToInt16(breakArray(228))
            returnArray(2) = Convert.ToInt16(breakArray(229))
            returnArray(3) = Convert.ToDouble(breakArray(219))
            returnArray(4) = Convert.ToDouble(breakArray(221))
            returnArray(5) = Convert.ToDouble(breakArray(222))
            returnArray(6) = Convert.ToDouble(breakArray(223))
            Return returnArray
        ElseIf Convert.ToInt16(breakArray(266)) > ColorRangeArray(MinIndex) And Convert.ToInt16(breakArray(266)) < ColorRangeArray(MaxIndex) And Convert.ToInt16(breakArray(267)) > 12 And Convert.ToInt16(breakArray(268)) > 10 Then
            returnArray(0) = Convert.ToInt16(breakArray(266))
            returnArray(1) = Convert.ToInt16(breakArray(267))
            returnArray(2) = Convert.ToInt16(breakArray(268))
            returnArray(3) = Convert.ToDouble(breakArray(258))
            returnArray(4) = Convert.ToDouble(breakArray(260))
            returnArray(5) = Convert.ToDouble(breakArray(261))
            returnArray(6) = Convert.ToDouble(breakArray(262))
            Return returnArray
        Else
            'If none of the clusters are the desired color
            returnArray(0) = 0
            Return returnArray
        End If

    End Function

    'If arduino code sends message through serial monitor
    Private Sub port_DataReceived(ByVal sender As Object, ByVal e As SerialDataReceivedEventArgs)
        'Split and display message
        messagereturn = Port.ReadExisting()
        messagereturn2 = messagereturn.Split(" ")

        'If demo is started
        If messagereturn2(0) = "demoStart" Then
            'Analyze image
            Invoke(Sub() UpdateLabel.Text = "Analyzing Image")
            TempDistance = messagereturn2(1)
            Dim colorA
            Invoke(Sub() colorA = GetColor())
            If colorA(0) = 0 Then
            Else
                'Show result to user
                Dim plantNumberTemp = messagereturn2(2) + 1
                PlantArea = (TempDistance * 1.6047) * colorA(3)
                Dim IntPlantArea As Integer = PlantArea * 1000
                PlantArea = IntPlantArea / 1000

                'Set labels
                Dim ColorLabelString As String = "Color Found = " + (colorA(2)).ToString + " with Area = " + (PlantArea).ToString + " Square Inches"
                Dim PlantLabelString As String = "Giving Plant " + (plantNumberTemp).ToString + " " + (AverageWaterArray(Convert.ToInt16(messagereturn2(2)))).ToString + " mL of Water"
                PlantLabel.Invoke(Sub() PlantLabel.Text = PlantLabelString)
                ColorLabel.Invoke(Sub() ColorLabel.Text = ColorLabelString)

                'Make button the color of plant
                DemoBtn.BackColor = Color.FromArgb(colorA(4), colorA(5), colorA(6))
                Invoke(Sub() UpdateLabel.Text = "Giving Water and Moving to Next Plant")

                'Send water volume to Arduino program
                Port.Write(AverageWaterArray(Convert.ToInt16(messagereturn2(2))))
                colorA = Nothing
            End If
        End If

        'If Arduino is requeting the color
        If messagereturn = "Color" Then
            Dim color = GetColor()
            ColorLabel = "Color: " + color(2)
            Port.Write(color)
        End If

        'If Arduino is requesting the average change using the dynamic linear regression function
        If messagereturn2(0) = "Average" Then
            Dim Slope = CalculateAverage(Convert.ToInt16(messagereturn2(1)), Convert.ToInt16(messagereturn2(2)), Convert.ToInt16(messagereturn2(3)), Convert.ToInt16(messagereturn2(4)))
            Port.Write(Slope)
        End If

        'If Arduino is requesting the area of the plant
        If messagereturn2(0) = "Distance" And Percentage > 0 Then
            PlantArea = (messagereturn2(1) * 1.6047) * Percentage
            PlantArea = PlantArea * 1000
            Port.Write(PlantArea)
        End If

        'If Arduino is giving plant watering and color details, send to database
        If messagereturn2(0) = "Update" Then
            printString = "insert into plant_water_details set plant_number = '" + messagereturn2(1) + "', water_volume = '" + messagereturn2(3) + "', color = '" + messagereturn2(2) + "';"
            CnExecute(printString)
            PlantLabel.Text = "Giving Plant " + messagereturn2(1) + " " + messagereturn(3) + "mL of water"
        End If
    End Sub

    'Search through database for data of specified plant
    Private Sub CollectPlantData(PlantNumber)

        Dim ObjReader As OdbcDataReader

        'Look only for data involving specific plant
        Dim StrSQL = "select * from plant_water_details where plant_number = "
        StrSQL += (PlantNumber + 1).ToString
        StrSQL += ";"
        ObjReader = CnExecuteReader(StrSQL)

        'Add data for all columns into lists to be passes to List2
        While ObjReader.Read
            Dim number = ObjReader.Item("plant_number")
            Dim water = ObjReader.Item("water_volume")
            Dim color = ObjReader.Item("color")
            Dim time = ObjReader.Item("date_time_collected")
            PlantWaterData.Add(water)
            PlantColorData.Add(color)
            PlantDateData.Add(time)
        End While

        ObjReader.Close()
        ObjReader = Nothing

    End Sub

    'Function to tun when plant buttons are clicked
    Private Sub PlantClick(Number)
        LabelsVisible()
        currentPlant = Number
        SetLabels(Number)
        PlantNumberPass = Number
        CollectPlantData(Number)
        wait(250)
        PlantForm.Show()
    End Sub

    'When plant buttons are clicked
    Private Sub Plant1_Click(sender As Object, e As EventArgs) Handles Plant1.Click
        PlantClick(0)
    End Sub

    Private Sub Plant2_Click(sender As Object, e As EventArgs) Handles Plant2.Click
        PlantClick(1)
    End Sub

    Private Sub Plant3_Click(sender As Object, e As EventArgs) Handles Plant3.Click
        PlantClick(2)
    End Sub

    Private Sub Plant4_Click(sender As Object, e As EventArgs) Handles Plant4.Click
        PlantClick(3)
    End Sub

    Private Sub Plant5_Click(sender As Object, e As EventArgs) Handles Plant5.Click
        PlantClick(4)
    End Sub

    Private Sub Plant6_Click(sender As Object, e As EventArgs) Handles Plant6.Click
        PlantClick(5)
    End Sub

    Private Sub Plant7_Click(sender As Object, e As EventArgs) Handles Plant7.Click
        PlantClick(6)
    End Sub

    Private Sub Plant8_Click(sender As Object, e As EventArgs) Handles Plant8.Click
        PlantClick(7)
    End Sub

    Private Sub Plant9_Click(sender As Object, e As EventArgs) Handles Plant9.Click
        PlantClick(8)
    End Sub

    Private Sub Plant10_Click(sender As Object, e As EventArgs) Handles Plant10.Click
        PlantClick(9)
    End Sub

    Private Sub Plant11_Click(sender As Object, e As EventArgs) Handles Plant11.Click
        PlantClick(10)
    End Sub

    Private Sub Plant12_Click(sender As Object, e As EventArgs) Handles Plant12.Click
        PlantClick(11)
    End Sub

    'Make labels visible
    Private Sub LabelsVisible()
        HealthComboBox.Text = ""
        ColorTextBox.Text = ""
        PlantLabel.Visible = True
        ColorLabel.Visible = True
        HealthLabel.Visible = True
        HealthComboBox.Visible = True
        ColorTextBox.Visible = True
    End Sub

    'Set the value of the text box and combo box based on collected data
    Private Sub SetLabels(inputNumber As Integer)
        If HealthArray(inputNumber) <> 2 Then
            If HealthArray(inputNumber) = 0 Then
                HealthComboBox.Text = "Dead"
            ElseIf HealthArray(inputNumber) = 1 Then
                HealthComboBox.Text = "Healthy"
            ElseIf HealthArray(inputNumber) = 3 Then
                HealthComboBox.Text = "Unhealthy"
            End If
        End If

        If ColorArray(inputNumber) <> -1 Then
            ColorTextBox.Text = ColorArray(inputNumber)
        End If

        Dim InputAdd As Integer = inputNumber + 1
        PlantLabel.Text = "Enter Information for Plant " + InputAdd.ToString()
        ColorLabel.Text = "Plant " + InputAdd.ToString() + " Color (HSV): "
        HealthLabel.Text = "Plant " + InputAdd.ToString() + " Health: "
    End Sub

    'If text box is changed
    Private Sub ColorTextBox_TextChanged(sender As Object, e As EventArgs) Handles ColorTextBox.TextChanged
        If ColorTextBox.Text <> "" Then
            ColorArray(currentPlant) = ColorTextBox.Text
        End If
        Dim plantNumber As Button
        If currentPlant = 0 Then
            plantNumber = Plant1
        ElseIf currentPlant = 1 Then
            plantNumber = Plant2
        ElseIf currentPlant = 2 Then
            plantNumber = Plant3
        ElseIf currentPlant = 3 Then
            plantNumber = Plant4
        ElseIf currentPlant = 4 Then
            plantNumber = Plant5
        ElseIf currentPlant = 5 Then
            plantNumber = Plant6
        ElseIf currentPlant = 6 Then
            plantNumber = Plant7
        ElseIf currentPlant = 7 Then
            plantNumber = Plant8
        ElseIf currentPlant = 8 Then
            plantNumber = Plant9
        ElseIf currentPlant = 9 Then
            plantNumber = Plant10
        ElseIf currentPlant = 10 Then
            plantNumber = Plant11
        ElseIf currentPlant = 11 Then
            plantNumber = Plant12
        End If
        ChangeColors(ColorArray(currentPlant), plantNumber)

    End Sub

    'If combo box is changed
    Private Sub HealthComboBox_SelectedIndexChanged(sender As Object, e As EventArgs) Handles HealthComboBox.SelectedIndexChanged
        If HealthComboBox.Text = "Healthy" Then
            HealthArray(currentPlant) = 1
        ElseIf HealthComboBox.Text = "Unhealthy" Then
            HealthArray(currentPlant) = 3
        ElseIf HealthComboBox.Text = "Dead" Then
            HealthArray(currentPlant) = 0
            ColorArray(currentPlant) = 0
            ColorTextBox.Text = "0"
        End If
    End Sub

    'If send button is clicked
    Private Sub SendBtn_Click(sender As Object, e As EventArgs) Handles SendBtn.Click
        Dim allow As Boolean = True

        'Check to see if all fields are filled out
        For counter = 0 To 11
            If ColorArray(counter) = -1 Then
                allow = False
            End If
            If HealthArray(counter) = 2 Then
                allow = False
            End If
        Next

        'What to do when fields are and not filled out
        If allow = False Then
            MessageBox.Show("Please complete required information for every plant", "Complete Form", MessageBoxButtons.OK)
        Else
            ColorTextBox.Enabled = False
            ColorTextBox.Visible = False
            HealthComboBox.Enabled = False
            HealthComboBox.Visible = False
            ColorLabel.Visible = False
            HealthLabel.Visible = False
            PlantLabel.Text = ""
            Sent = True

            'Send data to arduino program
            Dim ArduinoString As String = ""
            ArduinoString += "12 "
            For x = 0 To 11
                ArduinoString += ColorArray(x)
                ArduinoString += ","
                ArduinoString += HealthArray(x)
                ArduinoString += " "
            Next
            Port.Write(ArduinoString)
        End If

    End Sub

    'Chenge the color of plant buttons based on collected data
    Private Sub ChangeColors(color As Integer, btn As Button)
        If ColorTextBox.Text <> "" Then
            If color > 20 Then
                btn.BackColor = System.Drawing.Color.GreenYellow
            ElseIf color > 18 Then
                btn.BackColor = System.Drawing.Color.LimeGreen
            ElseIf color > 15 Then
                btn.BackColor = System.Drawing.Color.Green
            ElseIf color = 0 Then
                btn.BackColor = System.Drawing.Color.Red
            End If
        End If
    End Sub

    'Watering plant simulation
    Private Sub WaterPlant(plantNumber As Integer, button As Button)
        PlantLabel.Visible = True
        ColorLabel.Visible = True
        PlantLabel.Text = ("Giving plant #" + (plantNumber).ToString + " " + AverageWaterArray(plantNumber - 1).ToString + " mL of water")
        Dim Colorreturned = GetColor()
        ColorLabel.Text = ("Color = " + Colorreturned(2).ToString)
        button.BackColor = System.Drawing.Color.Blue
        wait(1000)
        button.BackColor = Color.FromArgb(Colorreturned(4), Colorreturned(5), Colorreturned(6))
        wait(500)
    End Sub

    'Delay
    Private Sub wait(ByVal interval As Integer)
        Dim sw As New Stopwatch
        sw.Start()
        Do While sw.ElapsedMilliseconds < interval
            'Allows interface to remain responsive
            Application.DoEvents()
        Loop
        sw.Stop()
    End Sub

    'For simulation
    Private Sub SimulateBtn_Click(sender As Object, e As EventArgs) Handles SimulateBtn.Click
        WaterPlant(1, Plant1)
        wait(5000)
        WaterPlant(2, Plant2)
        wait(5000)
        WaterPlant(3, Plant3)
        wait(5000)
        WaterPlant(4, Plant4)
        wait(5000)
        WaterPlant(5, Plant5)
        wait(5000)
        WaterPlant(6, Plant6)
        wait(5000)
        WaterPlant(7, Plant7)
        wait(5000)
        WaterPlant(8, Plant8)
        wait(5000)
        WaterPlant(9, Plant9)
        wait(5000)
        WaterPlant(10, Plant10)
        wait(5000)
        WaterPlant(11, Plant11)
        wait(5000)
        WaterPlant(12, Plant12)
        wait(5000)
    End Sub

    'For test camera feature
    Private Sub cmd3_Click(sender As Object, e As EventArgs) Handles cmd3.Click
        Dim colorreturned = GetColor()
        cmd3.BackColor = Color.FromArgb(colorreturned(4), colorreturned(5), colorreturned(6))
        Percentage = colorreturned(3)
    End Sub

    'For demo feature
    Private Sub DemoBtn_Click(sender As Object, e As EventArgs) Handles DemoBtn.Click
        'Show needed labels and hide unneeded labels
        ColorLabel.Enabled = True
        PlantLabel.Enabled = True
        ColorLabel.Visible = True
        PlantLabel.Visible = True
        ColorLabel.Text = ""
        PlantLabel.Text = ""
        UpdateLabel.Visible = True
        ColorTextBox.Visible = False
        HealthComboBox.Visible = False
        HealthLabel.Visible = False
        UpdateLabel.Text = "Starting Demo"

        'Send message to Arduino to start demo
        Port.Write("Demo")
    End Sub

    'If desired color is changed by user
    Private Sub ChooseColorBox_SelectedIndexChanged(sender As Object, e As EventArgs) Handles ChooseColorBox.SelectedIndexChanged
        If ColorLabel.Text = "Green" Then
            MinIndex = 0
            MaxIndex = 1
        ElseIf ColorLabel.Text = "Red" Then
            MinIndex = 2
            MaxIndex = 3
        ElseIf ColorLabel.Text = "Yellow" Then
            MinIndex = 4
            MaxIndex = 5
        End If
    End Sub
End Class