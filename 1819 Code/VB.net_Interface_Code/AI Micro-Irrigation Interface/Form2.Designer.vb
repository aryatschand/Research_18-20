<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class PlantForm
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.DataListView = New System.Windows.Forms.ListView()
        Me.PlantWater = CType(New System.Windows.Forms.ColumnHeader(), System.Windows.Forms.ColumnHeader)
        Me.PlantColor = CType(New System.Windows.Forms.ColumnHeader(), System.Windows.Forms.ColumnHeader)
        Me.PlantDate = CType(New System.Windows.Forms.ColumnHeader(), System.Windows.Forms.ColumnHeader)
        Me.ExitBtn = New System.Windows.Forms.Button()
        Me.PlantLabel = New System.Windows.Forms.Label()
        Me.SuspendLayout()
        '
        'DataListView
        '
        Me.DataListView.Columns.AddRange(New System.Windows.Forms.ColumnHeader() {Me.PlantWater, Me.PlantColor, Me.PlantDate})
        Me.DataListView.Location = New System.Drawing.Point(98, 32)
        Me.DataListView.Name = "DataListView"
        Me.DataListView.Size = New System.Drawing.Size(324, 316)
        Me.DataListView.TabIndex = 0
        Me.DataListView.UseCompatibleStateImageBehavior = False
        Me.DataListView.View = System.Windows.Forms.View.Details
        '
        'PlantWater
        '
        Me.PlantWater.Text = "Water (mL)"
        Me.PlantWater.Width = 84
        '
        'PlantColor
        '
        Me.PlantColor.Text = "Color"
        Me.PlantColor.Width = 73
        '
        'PlantDate
        '
        Me.PlantDate.Text = "Date/Time"
        Me.PlantDate.Width = 157
        '
        'ExitBtn
        '
        Me.ExitBtn.BackColor = System.Drawing.Color.Crimson
        Me.ExitBtn.ForeColor = System.Drawing.SystemColors.ControlText
        Me.ExitBtn.Location = New System.Drawing.Point(448, 32)
        Me.ExitBtn.Name = "ExitBtn"
        Me.ExitBtn.Size = New System.Drawing.Size(71, 57)
        Me.ExitBtn.TabIndex = 1
        Me.ExitBtn.Text = "Exit"
        Me.ExitBtn.UseVisualStyleBackColor = False
        '
        'PlantLabel
        '
        Me.PlantLabel.Location = New System.Drawing.Point(180, 9)
        Me.PlantLabel.Name = "PlantLabel"
        Me.PlantLabel.Size = New System.Drawing.Size(147, 13)
        Me.PlantLabel.TabIndex = 16
        Me.PlantLabel.Text = "Plant"
        Me.PlantLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'PlantForm
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(800, 450)
        Me.Controls.Add(Me.PlantLabel)
        Me.Controls.Add(Me.ExitBtn)
        Me.Controls.Add(Me.DataListView)
        Me.ImeMode = System.Windows.Forms.ImeMode.[On]
        Me.Name = "PlantForm"
        Me.Text = "Plant Data"
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents DataListView As ListView
    Friend WithEvents PlantColor As ColumnHeader
    Friend WithEvents PlantWater As ColumnHeader
    Friend WithEvents PlantDate As ColumnHeader
    Friend WithEvents ExitBtn As Button
    Friend WithEvents PlantLabel As Label
End Class
