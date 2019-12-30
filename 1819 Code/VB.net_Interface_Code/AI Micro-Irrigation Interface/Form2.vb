Public Class PlantForm
    Private Sub Form2_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        For x = 0 To Form1.PlantWaterData.Count - 1
            DataListView.Items.Add(New ListViewItem({Form1.PlantWaterData(x), Form1.PlantColorData(x), Form1.PlantDateData(x)}))
        Next
        PlantLabel.Text = "Showing Data From Plant " & (Form1.PlantNumberPass + 1).ToString
        Form1.PlantWaterData.Clear()
        Form1.PlantColorData.Clear()
        Form1.PlantDateData.Clear()
    End Sub

    Private Sub ExitBtn_Click(sender As Object, e As EventArgs) Handles ExitBtn.Click
        Me.Close()
    End Sub
End Class