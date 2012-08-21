// DialogFullScreen.cpp : 实现文件
//

#include "stdafx.h"
#include "GSNetClientDemo.h"
#include "DialogFullScreen.h"
#include "GSNetClientDemoDlg.h"
#include "../GSNetClient/GSNetClient.h"


// CDialogFullScreen 对话框

IMPLEMENT_DYNAMIC(CDialogFullScreen, CDialog)

CDialogFullScreen::CDialogFullScreen(CWnd* pParent /*=NULL*/)
	: CDialog(CDialogFullScreen::IDD, pParent)
{
	m_pParent = pParent;
}

CDialogFullScreen::~CDialogFullScreen()
{
}

void CDialogFullScreen::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CDialogFullScreen, CDialog)
	ON_WM_PAINT()
END_MESSAGE_MAP()


// CDialogFullScreen 消息处理程序

BOOL CDialogFullScreen::OnInitDialog()
{
	CDialog::OnInitDialog();

	MoveWindow(0, 0, GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN), TRUE);

	if(((CGSNetClientDemoDlg *)m_pParent)->m_hLiveRTSPHandle){
		GSNET_ClientSetWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hLiveRTSPHandle, m_hWnd);
		GSNET_ClientRefreshWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hLiveRTSPHandle);
	}
	else if(((CGSNetClientDemoDlg *)m_pParent)->m_hPlaybackHandle){
		GSNET_ClientSetWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hPlaybackHandle, m_hWnd);
		GSNET_ClientRefreshWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hPlaybackHandle);
	}

	return TRUE;  // return TRUE unless you set the focus to a control
	// 异常: OCX 属性页应返回 FALSE
}

void CDialogFullScreen::OnPaint()
{
	CPaintDC dc(this); // device context for painting
	RECT rect;
	GetWindowRect(&rect);

	CBrush brush(RGB(10, 10, 10));
	dc.FillRect(&rect, &brush);

	if(NULL != ((CGSNetClientDemoDlg *)m_pParent)->m_hLiveRTSPHandle)
	{
		GSNET_ClientRefreshWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hLiveRTSPHandle);
	}
	else if(NULL != ((CGSNetClientDemoDlg *)m_pParent)->m_hPlaybackHandle)
	{
		GSNET_ClientRefreshWnd(((CGSNetClientDemoDlg *)m_pParent)->m_hPlaybackHandle);
	}
}
