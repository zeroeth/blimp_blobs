#ifndef __GSNETCLIENT_H__
#define __GSNETCLIENT_H__

#include "GSNetStructDef.h"

//#define __BUILD_LIB

#if defined __BUILD_DLL
	#define GSNET_DLLAPI		extern "C" __declspec(dllexport)
#elif defined __BUILD_LIB
	#define GSNET_DLLAPI
#else
	#define GSNET_DLLAPI		extern "C" __declspec(dllimport)
#endif


/***************************PTZ******************************/
#define PTZ_STOP		0	/*	PTZ stop*/

#define TILT_UP		1	/* up */
#define TILT_DOWN		2	/* down */
#define PAN_LEFT		3	/* left */
#define PAN_RIGHT		4	/* right */


#define PT_LEFT_UP	5	/*  */
#define PT_LEFT_DOWN	6	/*  */
#define PT_RIGHT_UP	7	/*  */
#define PT_RIGHT_DOWN	8	/*  */

#define PTZ_ZOOM_IN		9 	/*  */
#define PTZ_ZOOM_OUT		10	/*  */
#define FOCUS_NEAR	11	/* */
#define FOCUS_FAR		12	/*  */
#define IRIS_OPEN		13	/*  */
#define IRIS_CLOSE	14	/*  */


#define GOTO_PRESET	15	/*  */
#define CLE_PRESET	16	/*  */
#define SET_PRESET	17	/*  */


#define PAN_AUTO		18	/* ÔÆÌ¨ÒÔSpeedµÄËÙ¶È×óÓÒÑ²º½ */
#define PAN_AUTO_STOP	19	/* Ñ²º½Í£Ö¹ */

extern "C"
{
/******************************************************************/

GSNET_DLLAPI BOOL __stdcall GSNET_Startup(UINT ulMessage, HWND hWnd, void (WINAPI *messagecallback)(LONG handle, int wParam, int lParam, void *context)=NULL, void* context=NULL);
GSNET_DLLAPI VOID __stdcall GSNET_Cleanup();
GSNET_DLLAPI BOOL __stdcall GSNET_SetWaitTime(int WaitTime=5, int TryNum=3, int TryInterval=10);
GSNET_DLLAPI VOID __stdcall GSNET_Log(const char *strFormat, ...);


GSNET_DLLAPI LONG __stdcall GSNET_ClientStart(CHANNEL_CLIENTINFO *m_pChaninfo);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStop(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStartView(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStopView(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientSetWnd(LONG hHandle, HWND hWnd);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientRefreshWnd(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientShowcallback(LONG hHandle, void(WINAPI *ShowCallBack)(BYTE *m_y, BYTE *m_u, BYTE *m_v, int stridey, int strideuv, int width, int height, void *context), void *context);
GSNET_DLLAPI LONG __stdcall GSNET_GetClientState(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_GetBitStreamInfo(LONG hHandle, ULONG *pBitRate, ULONG *pFrameRate);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientSetVideoParam(LONG hHandle, BYTE cbBrightness, BYTE cbContrast, BYTE cbSaturation);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientGetVideoParam(LONG hHandle, BYTE *pcbBrightness, BYTE *pcbContrast, BYTE *pcbSaturation);
GSNET_DLLAPI void __stdcall GSNET_ClientVerticalFlip(LONG hHandle, BOOL bVFlip);

GSNET_DLLAPI void __stdcall GSNET_ClientRotate180(LONG hHandle, BOOL bRotate180);


GSNET_DLLAPI BOOL __stdcall GSNET_ClientPlayAudio(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStopAudio(LONG hHandle);


GSNET_DLLAPI BOOL __stdcall GSNET_ClientCapturePicture(LONG hHandle, LPCTSTR filename);


GSNET_DLLAPI BOOL __stdcall GSNET_ClientStartRecord(LONG hHandle, LPCTSTR filename, DWORD dwDurationSeconds=0);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStopRecord(LONG hHandle);

GSNET_DLLAPI BOOL __stdcall GSNET_ClientPTZCtrl(LONG hHandle, int type, int param);


GSNET_DLLAPI BOOL __stdcall GSNET_ClientGetMDInfo(LONG hHandle, MOTION_DETECT_INFO* pMDInfo/*out*/);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientSaveMDInfo(LONG hHandle, MOTION_DETECT_INFO* pMDInfo/*in*/);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStartMD(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStopMD(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientStopAlarm(LONG hHandle, ULONG ulDeviceNum);
GSNET_DLLAPI BOOL __stdcall GSNET_ClientShowMDRegion(LONG hHandle, ULONG ulShow);


GSNET_DLLAPI BOOL __stdcall GSNET_ClientStartTalk(LONG hHandle);
GSNET_DLLAPI void __stdcall GSNET_ClientStopTalk(LONG hHandle);


GSNET_DLLAPI LONG __stdcall  GSNET_OpenFile(char* filename, HWND hWnd, BOOL bPause=FALSE);
GSNET_DLLAPI BOOL __stdcall  GSNET_CloseFile(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_ReplayPause(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_ReplayContinue(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_ReplayStepByStep(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_SpeedFast(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_SpeedNormal(LONG hHandle);
GSNET_DLLAPI BOOL __stdcall  GSNET_SpeedSlow(LONG hHandle);
GSNET_DLLAPI ULONG __stdcall GSNET_ReplayTotalTime(LONG hHandle);
GSNET_DLLAPI ULONG __stdcall GSNET_ReplayCurTime(LONG hHandle);
GSNET_DLLAPI BOOL  __stdcall GSNET_ReplaySeek(LONG hHandle, ULONG ulSeconds);
};






#endif


