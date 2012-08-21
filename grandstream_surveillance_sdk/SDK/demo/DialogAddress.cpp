// DialogAddress.cpp : 实现文件
//

#include "stdafx.h"
#include "GSNetClientDemo.h"
#include "DialogAddress.h"

// CDialogAddress 对话框

IMPLEMENT_DYNAMIC(CDialogAddress, CDialog)

CDialogAddress::CDialogAddress(CWnd* pParent /*=NULL*/)
	: CDialog(CDialogAddress::IDD, pParent)
{

}

CDialogAddress::~CDialogAddress()
{
}

void CDialogAddress::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_COMBO_CHANNEL, m_comboChannel);
	DDX_Control(pDX, IDC_EDIT1, m_ctrlIP);
	DDX_Control(pDX, IDC_COMBO_PROTOCOL, m_comboProtocol);
}


BEGIN_MESSAGE_MAP(CDialogAddress, CDialog)
	ON_BN_CLICKED(IDOK, &CDialogAddress::OnBnClickedOk)
	ON_BN_CLICKED(IDCANCEL, &CDialogAddress::OnBnClickedCancel)
END_MESSAGE_MAP()


// CDialogAddress 消息处理程序

void CDialogAddress::OnBnClickedOk()
{
	m_ctrlIP.GetWindowText(m_StrIPAddress);
	m_CurChannel = m_comboChannel.GetCurSel();
	m_Protocol   = m_comboProtocol.GetCurSel();

	OnOK();
}

void CDialogAddress::OnBnClickedCancel()
{
	OnCancel();
}

BOOL CDialogAddress::OnInitDialog()
{
	CDialog::OnInitDialog();

	m_ctrlIP.SetWindowText(m_StrIPAddress);
	m_comboChannel.AddString(_T("0"));
	m_comboChannel.AddString(_T("1"));
	m_comboChannel.AddString(_T("2"));
	m_comboChannel.AddString(_T("3"));
	m_comboChannel.AddString(_T("4"));
	m_comboChannel.AddString(_T("5"));
	m_comboChannel.AddString(_T("6"));
	m_comboChannel.AddString(_T("7"));
	m_comboChannel.SetCurSel(m_CurChannel);

	m_comboProtocol.AddString(_T("UDP"));
	m_comboProtocol.AddString(_T("TCP"));
	m_comboProtocol.SetCurSel(m_Protocol);

	return TRUE;  // return TRUE unless you set the focus to a control
	// 异常: OCX 属性页应返回 FALSE
}
