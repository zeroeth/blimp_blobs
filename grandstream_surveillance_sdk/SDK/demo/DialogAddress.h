#pragma once
#include "afxwin.h"


// CDialogAddress 对话框

class CDialogAddress : public CDialog
{
	DECLARE_DYNAMIC(CDialogAddress)

public:
	CDialogAddress(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~CDialogAddress();

// 对话框数据
	enum { IDD = IDD_DIALOG_ADDRESS };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()

public:
	CString		m_StrIPAddress;
	ULONG			m_CurChannel;
	ULONG			m_Protocol;
public:
	afx_msg void OnBnClickedOk();
public:
	afx_msg void OnBnClickedCancel();
public:
	virtual BOOL OnInitDialog();
public:
	CComboBox m_comboChannel;
public:
	CEdit m_ctrlIP;
public:
	CComboBox m_comboProtocol;
};
