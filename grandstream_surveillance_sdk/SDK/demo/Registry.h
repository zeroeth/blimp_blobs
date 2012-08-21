#if !defined(REGISTRY_H_INCLUDED_16B0FF9E_7147_46EB_84D8_C799D7FCB93A)
#define REGISTRY_H_INCLUDED_16B0FF9E_7147_46EB_84D8_C799D7FCB93A

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <winreg.h>

#define REG_RECT	0x0001
#define REG_POINT	0x0002

class CRegistry : public CObject
{
// Construction
public:
	CRegistry(HKEY hKeyRoot = HKEY_LOCAL_MACHINE);
	virtual ~CRegistry();

	struct REGINFO
	{
		LONG lMessage;
		DWORD dwType;
		DWORD dwSize;
	} m_Info;
// Operations
public:
	BOOL VerifyKey (HKEY hKeyRoot, LPCTSTR pszPath);
	BOOL VerifyKey (LPCTSTR pszPath);
	BOOL VerifyValue (LPCTSTR pszValue);
	BOOL CreateKey (HKEY hKeyRoot, LPCTSTR pszPath);
	BOOL Open (HKEY hKeyRoot, LPCTSTR pszPath);
	void Close();

	BOOL DeleteValue (LPCTSTR pszValue);
	BOOL DeleteValueKey (HKEY hKeyRoot, LPCTSTR pszPath);

	BOOL Write (LPCTSTR pszKey, int iVal);
	BOOL Write (LPCTSTR pszKey, DWORD dwVal);
	BOOL Write (LPCTSTR pszKey, LPCTSTR pszVal);
	BOOL Write (LPCTSTR pszKey, CStringList& scStringList);
	BOOL Write (LPCTSTR pszKey, CByteArray& bcArray);
	BOOL Write (LPCTSTR pszKey, CStringArray& scArray);
	BOOL Write (LPCTSTR pszKey, CDWordArray& dwcArray);
	BOOL Write (LPCTSTR pszKey, CWordArray& wcArray);
	BOOL Write (LPCTSTR pszKey, LPCRECT rcRect);
	BOOL Write (LPCTSTR pszKey, LPPOINT& lpPoint);

	BOOL Read (LPCTSTR pszKey, int& iVal);
	BOOL Read (LPCTSTR pszKey, DWORD& dwVal);
	BOOL Read (LPCTSTR pszKey, CString& sVal);
	BOOL Read (LPCTSTR pszKey, CStringList& scStringList);
	BOOL Read (LPCTSTR pszKey, CStringArray& scArray);
	BOOL Read (LPCTSTR pszKey, CDWordArray& dwcArray);
	BOOL Read (LPCTSTR pszKey, CWordArray& wcArray);
	BOOL Read (LPCTSTR pszKey, CByteArray& bcArray);
	BOOL Read (LPCTSTR pszKey, LPPOINT& lpPoint);
	BOOL Read (LPCTSTR pszKey, LPRECT& rcRect);

protected:	
	HKEY 	m_hKey;
	CString m_sPath;
};
#endif // !defined(REGISTRY_H_INCLUDED_16B0FF9E_7147_46EB_84D8_C799D7FCB93A)