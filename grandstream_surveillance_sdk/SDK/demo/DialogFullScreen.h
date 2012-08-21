#pragma once


// CDialogFullScreen 对话框

class CDialogFullScreen : public CDialog
{
	DECLARE_DYNAMIC(CDialogFullScreen)

public:
	CDialogFullScreen(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~CDialogFullScreen();

// 对话框数据
	enum { IDD = IDD_DIALOG_FULL_SCREEN };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
public:
	virtual BOOL OnInitDialog();

private:
	void	*m_pParent;
	afx_msg void OnPaint();
};
