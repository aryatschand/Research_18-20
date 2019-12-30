Option Explicit On
Option Strict Off

Imports System
Imports System.Drawing

Imports System.Runtime
Imports System.Runtime.InteropServices

Module modGraph

    Public Function InvertPicturesFromCapturedWindow() As Bitmap
        Dim InvertImages As Bitmap
        Dim InvertdataCopy As IDataObject

        Dim X As Integer
        Dim Y As Integer
        Dim r As Integer
        Dim g As Integer
        Dim b As Integer

        SendMessage(hHwnd, WM_CAP_EDIT_COPY, 0, 0)
        InvertdataCopy = Clipboard.GetDataObject()

        InvertImages = CType(InvertdataCopy.GetData(GetType(System.Drawing.Bitmap)), Image)

        X = 0
        Y = 0
        r = 0
        g = 0
        b = 0

        For X = 0 To InvertImages.Width - 1
            For Y = 0 To InvertImages.Height - 1
                r = 255 - InvertImages.GetPixel(X, Y).R
                g = 255 - InvertImages.GetPixel(X, Y).G
                b = 255 - InvertImages.GetPixel(X, Y).B

                InvertImages.SetPixel(X, Y, Color.FromArgb(r, g, b))
            Next Y
        Next X

        InvertdataCopy = Nothing

        Return InvertImages
        InvertImages.Dispose()
    End Function

    Public Function GrayScalePicture() As Bitmap
        On Error Resume Next
        Dim bmGrayScale As Bitmap
        Dim GrayScaleData As IDataObject

        Dim X As Integer
        Dim Y As Integer
        Dim colorX As Integer

        SendMessage(hHwnd, WM_CAP_EDIT_COPY, 0, 0)
        GrayScaleData = Clipboard.GetDataObject()
        bmGrayScale = CType(GrayScaleData.GetData(GetType(System.Drawing.Bitmap)), Image)

        X = 0
        Y = 0

        For X = 0 To bmGrayScale.Width - 1
            For Y = 0 To bmGrayScale.Height - 1

                colorX = (CInt(bmGrayScale.GetPixel(X, Y).R) +
                   bmGrayScale.GetPixel(X, Y).G +
                   bmGrayScale.GetPixel(X, Y).B) \ 3

                bmGrayScale.SetPixel(X, Y, Color.FromArgb(colorX, colorX, colorX))
            Next Y
        Next X

        GrayScaleData = Nothing

        Return bmGrayScale
        bmGrayScale.Dispose()
    End Function

    Public Function SephiaRed() As Bitmap
        On Error Resume Next
        Dim SephiaRedBmp As Bitmap
        Dim SephiaRedData As IDataObject

        Dim X As Integer
        Dim Y As Integer
        Dim r As Integer
        Dim g As Integer
        Dim b As Integer

        SendMessage(hHwnd, WM_CAP_EDIT_COPY, 0, 0)
        SephiaRedData = Clipboard.GetDataObject()

        SephiaRedBmp = CType(SephiaRedData.GetData(GetType(System.Drawing.Bitmap)), Image)

        X = 0
        Y = 0
        r = 0
        g = 0
        b = 0

        'Change This Value To Sephia Red
        For X = 0 To SephiaRedBmp.Width - 1
            For Y = 0 To SephiaRedBmp.Height - 1
                r = 255 - SephiaRedBmp.GetPixel(X, Y).R
                g = 255 - SephiaRedBmp.GetPixel(X, Y).G / 3
                b = 255 - SephiaRedBmp.GetPixel(X, Y).B / 3

                SephiaRedBmp.SetPixel(X, Y, Color.FromArgb(r, g, b))
            Next Y
        Next X

        SephiaRedData = Nothing

        Return SephiaRedBmp
        SephiaRedBmp.Dispose()
    End Function

    Public Function DetectMovement() As Long
        On Error Resume Next

        Dim detectPicture As Bitmap
        Dim DetectData As IDataObject

        Dim X As Integer
        Dim Y As Integer
        Dim Tolerance As Integer
        Dim inter As Integer
        Dim r1, r2, g1, g2, b1, b2 As Integer
        Dim Color1, Color2 As Color

        SendMessage(hHwnd, WM_CAP_EDIT_COPY, 0, 0)
        DetectData = Clipboard.GetDataObject()

        detectPicture = CType(DetectData.GetData(GetType(System.Drawing.Bitmap)), Image)

        Tolerance = 15
        inter = 10
        X = 0 : Y = 0
        r1 = 0 : r2 = 0 : g1 = 0 : g2 = 0 : b1 = 0 : b2 = 0
        Color1 = Nothing : Color2 = Nothing

        Dim MValue(0 To detectPicture.Width, 0 To detectPicture.Height) As Boolean

        For X = 0 To detectPicture.Width / inter - 1
            For Y = 0 To detectPicture.Height / inter - 1
                Color1 = detectPicture.GetPixel(X * inter, Y * inter)
                r1 = Color1.R
                g1 = Color1.G
                b1 = Color1.B

                r2 = Color2.R
                g2 = Color2.G
                b2 = Color2.B
                If System.Math.Abs(r1 - r2) < Tolerance And System.Math.Abs(g1 - g2) < Tolerance And System.Math.Abs(b1 - b2) < Tolerance Then
                    'Remain
                    MValue(X, Y) = True
                Else
                    'Moved
                    Color2 = detectPicture.GetPixel(X * inter, Y * inter)
                    MValue(X, Y) = False
                End If
            Next Y
        Next X
        X = 0
        Y = 0

        Dim RealRi As Long = 0
        For X = 1 To detectPicture.Width / inter - 2
            For Y = 1 To detectPicture.Height / inter - 2
                If MValue(X, Y + 1) = False Then
                    If MValue(X, Y - 1) = False Then
                        If MValue(X + 1, Y) = False Then
                            If MValue(X - 1, Y) = False Then
                                RealRi = RealRi + 1
                            End If
                        End If
                    End If
                End If
            Next
        Next

        Return RealRi
        detectPicture.Dispose()
    End Function

End Module
