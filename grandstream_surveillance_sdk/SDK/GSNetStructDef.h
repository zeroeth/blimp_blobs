#ifndef __GSNETSTRUCTDEF_H__
#define __GSNETSTRUCTDEF_H__

#define MAX_SERVER_NAME_LEN			32
#define MAX_USER_NAME_LEN			32
#define MAX_PASSWORD_LEN			64

#define MAX_FILENAME_LEN			255

enum{
	PROTOCOL_RTSP_UDP   = 0,
	PROTOCOL_RTSP_TCP   = 1,
	PROTOCOL_RTSP_MCAST = 2,//(reserved)
};

typedef struct{
	WORD m_protocol;				//(reserved)
	WORD m_playstart;               //if 0, video is hide; if 1, video is show(normally, set this parameter 1) 
	BYTE m_ch;                      //channel 
	HWND m_hVideohWnd;              //window handle of shown video
	HWND m_hChMsgWnd;               //(reserved)
	UINT m_nChMsgID;                //(reserved)
	int  m_buffnum;                 
	int  m_useoverlay;              //(reserved)
	COLORREF nColorKey;             //color key (reserved)
	
	void *lpReserv;						
	void *callbackContext;                  //callback context a important param*

	char url[128];							//eg: 192.168.83.254:554   or  www.abcdef.com:554
	char m_sername[MAX_SERVER_NAME_LEN+1];  //reserved
	char m_username[MAX_USER_NAME_LEN+1];   //user name
	char m_password[MAX_PASSWORD_LEN+1];    //password
}CHANNEL_CLIENTINFO;

#define MAX_MOTION_REGION		16
typedef struct{
	BYTE	cbSensitive[MAX_MOTION_REGION];
	RECT	rcRegion[MAX_MOTION_REGION];
}MOTION_DETECT_INFO;


/**********************************************************/

/********************link message************************/
/*wParam*/
#define GSMSG_LINKMSG			1		

/*lParam*/
#define GSMSG_LINKMSG_OK				0	//successful
#define GSMSG_LINKMSG_CONNECTING		1   //connecting, you can Ignore this message, normally
#define GSMSG_LINKMSG_FAILED			2	//connect failed
#define GSMSG_LINKMSG_DISCONNECT		3	//disconnect
#define GSMSG_LINKMSG_RECONNECT			4   //reconnect
#define GSMSG_LINKMSG_PLAYFAILED		5   //play failed and give up reconnect
/******************************************************/

/********************motion detect*********************/
/*wParam*/
#define GSMSG_RECORD			6		//record state
/*lParm*/
#define GSMSG_RECORD_BEGIN_NORMAL_RECORD		0// you can Ignore this message, normally
#define GSMSG_RECORD_END_NORMAL_RECORD			1// you can Ignore this message, normally	
#define GSMSG_RECORD_BEGIN_ALARM_RECORD			2// you can Ignore this message, normally
#define GSMSG_RECORD_END_ALARM_RECORD			3// you can Ignore this message, normally
#define GSMSG_RECORD_NORMAL_PACKET_FINISH		4//if you set record duration you must process this message to start other record-file.
#define GSMSG_RECORD_ALARM_PACKET_FINISH		5// you can Ignore this message, normally
/******************************************************/

/*wParam*/
#define GSMSG_VIDEOMOTION		2		//motion detect
#define GSMSG_VIDEOLOST			3 		//video lost (reserved)
#define GSMSG_ALARM				4		//probe alarm
#define GSMSG_OUTPUTSTATUS		5		//(reserved)
#define GSMSG_REPLAY_END		7		//replay file complete
#endif




