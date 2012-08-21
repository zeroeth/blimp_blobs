// GSNetClientDemoDlg.h : 头文件
//

#pragma once
#include "afxcmn.h"
#include "afxwin.h"


#define WM_GSMSG_ID			(WM_USER+100)


// CGSNetClientDemoDlg 对话框
class CGSNetClientDemoDlg : public CDialog
{
// 构造
public:
	CGSNetClientDemoDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
	enum { IDD = IDD_GSNETCLIENTDEMO_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
//	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButtonOpenFile();
public:
	afx_msg void OnBnClickedButtonCloseFile();

protected:

	afx_msg void OnClose();
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnPaint();
	afx_msg void OnBnClickedButtonLiveRtsp();
	afx_msg void OnBnClickedButtonStopLiveRtsp();
	afx_msg void OnBnClickedButtonStartRecord();
	afx_msg void OnBnClickedButtonStopRecord();
	afx_msg void OnBnClickedButtonCapture();
	afx_msg void OnBnClickedButtonFull();
	afx_msg void OnBnClickedButtonVpGet();
	afx_msg void OnBnClickedButtonVpSet();
	afx_msg void OnBnClickedButtonStartView();
	afx_msg void OnBnClickedButtonStopView();
	afx_msg void OnBnClickedButtonAlarmRecord();
	afx_msg void OnBnClickedButtonFast();
	afx_msg void OnBnClickedButtonSlow();
	afx_msg void OnBnClickedButtonNormal();
	afx_msg void OnBnClickedButtonPause();
	afx_msg void OnBnClickedButtonStep();
	afx_msg void OnBnClickedButtonSeek();
	afx_msg void OnBnClickedButtonContinue();
	afx_msg void OnBnClickedButtonStartTalk();
	afx_msg void OnBnClickedButtonZoomIn();
	afx_msg void OnBnClickedButtonZoomOut();
	afx_msg void OnBnClickedButtonSound();
	afx_msg void OnLButtonDblClk(UINT nFlags, CPoint point);
	afx_msg void OnBnClickedButtonRefreshWnd();

	virtual LRESULT WindowProc(UINT message, WPARAM wParam, LPARAM lParam);
public:
	virtual BOOL OnCmdMsg(UINT nID, int nCode, void* pExtra, AFX_CMDHANDLERINFO* pHandlerInfo);
	BOOL HitTest(int nID, CPoint point);
	LONG	m_hLiveRTSPHandle;
	LONG	m_hPlaybackHandle;
private:


	CString m_strURL;
	ULONG	m_channel;
	ULONG	m_protocol;
	BOOL	m_bSmooth;
	
	CSpinButtonCtrl m_ctrlSpinBrightness;
	CEdit m_ctrlBrightness;

	CSpinButtonCtrl m_ctrlSpinContrast;
	CEdit m_ctrlContrast;

	CSpinButtonCtrl m_ctrlSpinSaturation;
	CEdit m_ctrlSaturation;

	TCHAR	m_contextTest[128];

};
