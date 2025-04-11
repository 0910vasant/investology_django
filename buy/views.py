from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import logging
logger = logging.getLogger()
from django.contrib import messages
from django.http import JsonResponse
from crm.models import *
from app.models import *
from buy.models import *
from django.contrib import messages #import messages
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum

import pandas as pd
from itertools import chain

def send_login_dtl(request):
    data = {
        "sendResponseFormat"    : "JSON",
        "loginid"               : "EASYINVUAT",
        "password"              : "T7BO43drYUA0WrCASXo75g==",
        "entityId"              : "40007K",
        "logTp"                 : "A",
        "versionNo"             : "1.00"
    }
    return JsonResponse(data,safe=False,status=200)


@api_view(["POST"])
def add_buy_api(request):
    try:
        login_id                = request.data.get("login_id")
        sendResponseFormat      = request.data.get("sendResponseFormat")
        sessioncontext          = request.data.get("sessioncontext")
        sendersubid             = request.data.get("sendersubid")
        logTp                   = request.data.get("logTp")
        versionNo               = request.data.get("versionNo")
        actionType              = request.data.get("actionType")
        txnType                 = request.data.get("txnType")
        orderMode               = request.data.get("orderMode")
        tranSource              = request.data.get("tranSource")
        folioTxnFlag            = request.data.get("folioTxnFlag")
        txnEvent                = request.data.get("txnEvent")
        pageForRole             = request.data.get("pageForRole")
        can                     = request.data.get("can")
        jointHolderFlag         = request.data.get("jointHolderFlag")
        holderDetail            = request.data.get("holderDetail")
        directFlag              = request.data.get("directFlag")
        riaFlag                 = request.data.get("riaFlag")
        riaCode                 = request.data.get("riaCode")
        arnType                 = request.data.get("arnType")
        arnCode                 = request.data.get("arnCode")
        subBrkArnLabel          = request.data.get("subBrkArnLabel")
        subBrkArnType           = request.data.get("subBrkArnType")
        subBrkArnCode           = request.data.get("subBrkArnCode")
        subBrokCode             = request.data.get("subBrokCode")
        branchRMInternalCode    = request.data.get("branchRMInternalCode")
        euincode                = request.data.get("euincode")
        euinDeclaration         = request.data.get("euinDeclaration")
        depositoryFlag          = request.data.get("depositoryFlag")
        dpType                  = request.data.get("dpType")
        invDpAccNo              = request.data.get("invDpAccNo")
        paymentFlag             = request.data.get("paymentFlag")
        payment_instrumentType  = request.data.get("payment_instrumentType")
        payment_bankId          = request.data.get("payment_bankId")
        payment_invAccType      = request.data.get("payment_invAccType")
        payment_micrNo          = request.data.get("payment_micrNo")
        payment_ifscCode        = request.data.get("payment_ifscCode")
        instDate                = request.data.get("instDate")
        payment_invAccNo        = request.data.get("payment_invAccNo")
        payment_TxnDoneFlag     = request.data.get("payment_TxnDoneFlag")
        paymentRefNo            = request.data.get("paymentRefNo")
        payment_newVANFlag      = request.data.get("payment_newVANFlag")
        payment_VirtAccNo       = request.data.get("payment_VirtAccNo")
        paymentAmount           = request.data.get("paymentAmount")
        totalAmount             = request.data.get("totalAmount")
        extGroupRefNo           = request.data.get("extGroupRefNo")
        noOfSchemes             = request.data.get("noOfSchemes")

        subsequentpaymentflag   = request.data.get("subsequentpaymentflag")
        subseq_existotmflag     = request.data.get("subseq_existotmflag")
        subseq_invacctype       = request.data.get("subseq_invacctype")
        subseq_invaccno         = request.data.get("subseq_invaccno")
        subseq_micrno           = request.data.get("subseq_micrno")
        subseq_ifsccode         = request.data.get("subseq_ifsccode")
        subseq_bankid           = request.data.get("subseq_bankid")
        subseq_instrumenttype   = request.data.get("subseq_instrumenttype")
        subseq_maximumamount    = request.data.get("subseq_maximumamount")
        subseq_perpetualflag    = request.data.get("subseq_perpetualflag")
        subseq_startdate        = request.data.get("subseq_startdate")
        subseq_enddate          = request.data.get("subseq_enddate")
        subseq_paymentrefno     = request.data.get("subseq_paymentrefno")
        grouporderno            = request.data.get("grouporderno")
        applinkprim             = request.data.get("applinkprim")
        netbankinglink          = request.data.get("netbankinglink")
        folionumber          = request.data.get("folionumber")
        
        
        holdNat                 = request.data.get("holdNat")
        taxStatus               = request.data.get("taxStatus")
        priPanOrPekrn           = request.data.get("priPanOrPekrn")
        secPanOrPekrn           = request.data.get("secPanOrPekrn")
        thrPanOrPekrn           = request.data.get("thrPanOrPekrn")
        gurPanOrPekrn           = request.data.get("gurPanOrPekrn")

        recordNo                = request.data.getlist("recordNo[]")
        extUniqueRefId          = request.data.getlist("extUniqueRefId[]")
        folioAccNo              = request.data.getlist("folioAccNo[]")
        folioCheckDigit         = request.data.getlist("folioCheckDigit[]")
        rtaAmcCode              = request.data.getlist("rtaAmcCode[]")
        rtaSchemeCode           = request.data.getlist("rtaSchemeCode[]")

        srcSchemeCode           = request.data.getlist("srcSchemeCode[]")
        tarSchemeCode           = request.data.getlist("tarSchemeCode[]")

        dividendOption          = request.data.getlist("dividendOption[]")
        txnVolumeType           = request.data.getlist("txnVolumeType[]")
        txnVolume               = request.data.getlist("txnVolume[]")

        frequency               = request.data.getlist("frequency[]")
        day                     = request.data.getlist("day[]")
        start_Month             = request.data.getlist("start_Month[]")
        start_Year              = request.data.getlist("start_Year[]")
        end_Month               = request.data.getlist("end_Month[]")
        end_Year                = request.data.getlist("end_Year[]")
        

        logger.info(f"""    
            login_id                = {login_id}
            sendResponseFormat      = {sendResponseFormat}
            sessioncontext          = {sessioncontext}
            sendersubid             = {sendersubid}
            logTp                   = {logTp}
            versionNo               = {versionNo}
            actionType              = {actionType}
            txnType                 = {txnType}
            orderMode               = {orderMode}
            tranSource              = {tranSource}
            folioTxnFlag            = {folioTxnFlag}
            txnEvent                = {txnEvent}
            pageForRole             = {pageForRole}
            can                     = {can}
            jointHolderFlag         = {jointHolderFlag}
            holderDetail            = {holderDetail}
            directFlag              = {directFlag}
            riaFlag                 = {riaFlag}
            riaCode                 = {riaCode}
            arnType                 = {arnType}
            arnCode                 = {arnCode}
            subBrkArnLabel          = {subBrkArnLabel}
            subBrkArnType           = {subBrkArnType}
            subBrkArnCode           = {subBrkArnCode}
            subBrokCode             = {subBrokCode}
            branchRMInternalCode    = {branchRMInternalCode}
            euincode                = {euincode}
            euinDeclaration         = {euinDeclaration}
            depositoryFlag          = {depositoryFlag}
            dpType                  = {dpType}
            invDpAccNo              = {invDpAccNo}
            paymentFlag             = {paymentFlag}
            payment_instrumentType  = {payment_instrumentType}
            payment_bankId          = {payment_bankId}
            payment_invAccType      = {payment_invAccType}
            payment_micrNo          = {payment_micrNo}
            payment_ifscCode        = {payment_ifscCode}
            instDate                = {instDate}
            payment_invAccNo        = {payment_invAccNo}
            payment_TxnDoneFlag     = {payment_TxnDoneFlag}
            paymentRefNo            = {paymentRefNo	}
            payment_newVANFlag      = {payment_newVANFlag}
            payment_VirtAccNo       = {payment_VirtAccNo}
            paymentAmount           = {paymentAmount}
            totalAmount             = {totalAmount}
            extGroupRefNo           = {extGroupRefNo}
            noOfSchemes             = {noOfSchemes}
            holdNat                 = {holdNat}
            taxStatus               = {taxStatus}
            priPanOrPekrn           = {priPanOrPekrn}
            secPanOrPekrn           = {secPanOrPekrn}
            thrPanOrPekrn           = {thrPanOrPekrn}
            gurPanOrPekrn           = {gurPanOrPekrn}
            subsequentpaymentflag   = {subsequentpaymentflag}
            subseq_existotmflag     = {subseq_existotmflag}
            subseq_invacctype       = {subseq_invacctype}
            subseq_invaccno         = {subseq_invaccno}
            subseq_micrno           = {subseq_micrno}
            subseq_ifsccode         = {subseq_ifsccode}
            subseq_bankid           = {subseq_bankid}
            subseq_instrumenttype   = {subseq_instrumenttype}
            subseq_maximumamount    = {subseq_maximumamount}
            subseq_perpetualflag    = {subseq_perpetualflag}
            subseq_startdate        = {subseq_startdate}
            subseq_enddate          = {subseq_enddate}
            subseq_paymentrefno     = {subseq_paymentrefno}
            grouporderno            = {grouporderno}
            applinkprim             = {applinkprim}
            netbankinglink          = {netbankinglink}
            folionumber             = {folionumber}
        """)
        logger.info(f"""
            recordNo                = {recordNo}
            extUniqueRefId          = {extUniqueRefId}
            folioAccNo              = {folioAccNo}
            folioCheckDigit         = {folioCheckDigit}
            rtaAmcCode              = {rtaAmcCode}
            rtaSchemeCode           = {rtaSchemeCode}
            srcSchemeCode           = {srcSchemeCode}
            tarSchemeCode           = {tarSchemeCode}
            dividendOption          = {dividendOption}
            txnVolumeType           = {txnVolumeType}
            txnVolume               = {txnVolume}
            frequency               = {frequency}
            day                     = {day}
            start_Month             = {start_Month}
            start_Year              = {start_Year}
            end_Month               = {end_Month}
            end_Year                = {end_Year}
        """)
        # EMPLOYEE_CODE           = 
        add = Buy.objects.create(
            USER                    = Registration_personal_details.objects.get(id=login_id),
            SENDRESPONSEFORMAT      = sendResponseFormat ,
            SESSIONCONTEXT          = sessioncontext ,
            SENDERSUBID             = sendersubid ,
            LOGTP                   = logTp ,
            VERSIONNO               = versionNo ,
            ACTIONTYPE              = actionType ,
            TXNTYPE                 = txnType ,
            ORDERMODE               = orderMode ,
            TRANSOURCE              = tranSource ,
            FOLIOTXNFLAG            = folioTxnFlag ,
            TXNEVENT                = txnEvent ,
            PAGEFORROLE             = pageForRole ,
            CAN                     = can ,
            JOINTHOLDERFLAG         = jointHolderFlag ,
            HOLDERDETAIL            = holderDetail ,
            DIRECTFLAG              = directFlag ,
            RIAFLAG                 = riaFlag ,
            RIACODE                 = riaCode ,
            ARNTYPE                 = arnType ,
            ARNCODE                 = arnCode ,
            SUBBRKARNLABEL          = subBrkArnLabel ,
            SUBBRKARNTYPE           = subBrkArnType ,
            SUBBRKARNCODE           = subBrkArnCode ,
            SUBBROKCODE             = subBrokCode ,
            BRANCHRMINTERNALCODE    = branchRMInternalCode ,
            EUINCODE                = euincode ,
            EUINDECLARATION         = euinDeclaration ,
            DEPOSITORYFLAG          = depositoryFlag ,
            DPTYPE                  = dpType ,
            INVDPACCNO              = invDpAccNo ,
            PAYMENTFLAG             = paymentFlag ,
            PAYMENT_INSTRUMENTTYPE  = payment_instrumentType ,
            PAYMENT_BANKID          = payment_bankId ,
            PAYMENT_INVACCTYPE      = payment_invAccType ,
            PAYMENT_MICRNO          = payment_micrNo ,
            PAYMENT_IFSCCODE        = payment_ifscCode ,
            INSTDATE                = instDate ,
            PAYMENT_INVACCNO        = payment_invAccNo ,
            PAYMENT_TXNDONEFLAG     = payment_TxnDoneFlag ,
            PAYMENTREFNO            = paymentRefNo	 ,
            PAYMENT_NEWVANFLAG      = payment_newVANFlag ,
            PAYMENT_VIRTACCNO       = payment_VirtAccNo ,
            PAYMENTAMOUNT           = paymentAmount ,
            TOTALAMOUNT             = totalAmount ,
            EXTGROUPREFNO           = extGroupRefNo ,
            NOOFSCHEMES             = noOfSchemes ,
            HOLDNAT                 = holdNat ,
            TAXSTATUS               = taxStatus ,
            PRIPANORPEKRN           = priPanOrPekrn ,
            SECPANORPEKRN           = secPanOrPekrn ,
            THRPANORPEKRN           = thrPanOrPekrn ,
            GURPANORPEKRN           = gurPanOrPekrn ,
            GROUPORDERNO            = grouporderno,
            APPLINKPRIM             = applinkprim,
            NETBANKINGLINK          = netbankinglink,
            FOLIONUMBER             = folionumber
        )

        for i in range(len(recordNo)):
            abs = Buy_schemes.objects.create(
            BUY                     = add ,
            RECORDNO                = recordNo[i] ,
            EXTUNIQUEREFID          = extUniqueRefId[i] ,
            FOLIOACCNO              = folioAccNo[i] ,
            FOLIOCHECKDIGIT         = folioCheckDigit[i] ,
            RTAAMCCODE              = rtaAmcCode[i] ,
            DIVIDENDOPTION          = dividendOption[i] ,
            TXNVOLUME_TYPE          = txnVolumeType[i],
            TXNVOLUME               = txnVolume[i] ,
            )
            if txnType != "E" and txnType != "S":
                abs.RTASCHEMECODE           = rtaSchemeCode[i]
            
            if txnType == "E":
                abs.SRCSCHEMECODE   = srcSchemeCode[i]
                abs.TARSCHEMECODE   = tarSchemeCode[i]

            if txnType == "V" or txnType == "E" or txnType == "J":
                abs.FREQUENCY       = frequency[i]
                abs.DAY             = day[i]
                abs.START_MONTH     = start_Month[i]
                abs.START_YEAR      = start_Year[i]
                abs.END_MONTH       = end_Month[i]
                abs.END_YEAR        = end_Year[i]
                abs.save()
        return JsonResponse("Buy Add Sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)

@api_view(["POST"])
def add_redeem_api(request):
    try:
        login_id            = request.data.get("login_id")
        sendresponseformat  = request.data.get("sendResponseFormat")
        sessioncontext      = request.data.get("sessioncontext")
        sendersubid         = request.data.get("sendersubid")
        logtp               = request.data.get("logTp")
        versionno           = request.data.get("versionNo")
        txntype             = request.data.get("txnType")
        ordermode           = request.data.get("orderMode")
        transource          = request.data.get("tranSource")
        actiontype          = request.data.get("actionType")
        foliotxnflag        = request.data.get("folioTxnFlag")
        txnevent            = request.data.get("txnEvent")
        pageforrole         = request.data.get("pageForRole")
        can                 = request.data.get("can")
        jointholderflag     = request.data.get("jointHolderFlag")
        holderdetail        = request.data.get("holderDetail")
        noofschemes         = request.data.get("noOfSchemes")

        recordNo            = request.data.getlist("recordNo[]")
        extUniqueRefId      = request.data.getlist("extUniqueRefId[]")
        folioAccNo          = request.data.getlist("folioAccNo[]")
        folioCheckDigit     = request.data.getlist("folioCheckDigit[]")
        rtaAmcCode          = request.data.getlist("rtaAmcCode[]")
        rtaSchemeCode       = request.data.getlist("rtaSchemeCode[]")
        # dividendOption      = request.data.getlist("dividendOption")
        txnVolumeType       = request.data.getlist("txnVolumeType[]")
        txnVolume           = request.data.getlist("txnVolume[]")
        payoutFlag          = request.data.getlist("payoutFlag[]")
        invAccNo            = request.data.getlist("invAccNo[]")
        micrNo              = request.data.getlist("micrNo[]")
        ifscCode            = request.data.getlist("ifscCode[]")

        frequency           = request.data.getlist("frequency[]")
        day                 = request.data.getlist("day[]")
        start_Month         = request.data.getlist("start_Month[]")
        start_Year          = request.data.getlist("start_Year[]")
        end_Month           = request.data.getlist("end_Month[]")
        end_Year            = request.data.getlist("end_Year[]")
        grouporderno       = request.data.get("grouporderno")

        logger.info(f"""
            login_id           = {login_id}
            sendresponseformat = {sendresponseformat }
            sessioncontext     = {sessioncontext}
            sendersubid        = {sendersubid}
            logtp              = {logtp}
            versionno          = {versionno}
            actiontype         = {actiontype}
            txntype            = {txntype}
            ordermode          = {ordermode}
            transource         = {transource}
            foliotxnflag       = {foliotxnflag}
            txnevent           = {txnevent}
            pageforrole        = {pageforrole}
            can                = {can}
            jointholderflag     = {jointholderflag}
            holderdetail        = {holderdetail}
            noofschemes         = {noofschemes}
            recordNo            = {recordNo}
            extUniqueRefId      = {extUniqueRefId}
            folioAccNo          = {folioAccNo}
            folioCheckDigit     = {folioCheckDigit}
            rtaAmcCode          = {rtaAmcCode}
            rtaSchemeCode       = {rtaSchemeCode}
            txnVolumeType       = {txnVolumeType}
            txnVolume           = {txnVolume}
            payoutFlag          = {payoutFlag}
            invAccNo            = {invAccNo}
            micrNo              = {micrNo}
            ifscCode            = {ifscCode}

            frequency           = {frequency}
            day                 = {day}
            start_Month         = {start_Month}
            start_Year          = {start_Year}
            end_Month           = {end_Month}
            end_Year            = {end_Year}
            grouporderno        = {grouporderno}
        """)
        add = Redeem.objects.create(
            USER                = Registration_personal_details.objects.get(id=login_id),
            SENDRESPONSEFORMAT  = "JSON"  ,
            SESSIONCONTEXT      = sessioncontext ,
            SENDERSUBID         = sendersubid ,
            LOGTP               = logtp ,
            VERSIONNO           = versionno ,
            TXNTYPE             = txntype ,
            ORDERMODE           = ordermode ,
            TRANSOURCE          = transource ,
            ACTIONTYPE          = actiontype ,
            FOLIOTXNFLAG        = foliotxnflag ,
            TXNEVENT            = txnevent ,
            PAGEFORROLE         = pageforrole ,
            CAN                 = can ,
            JOINTHOLDERFLAG     = jointholderflag,
            HOLDERDETAIL        = holderdetail,
            NOOFSCHEMES         = noofschemes ,
            GROUPORDERNO        = grouporderno,
        )
        for i in range(len(recordNo)):
            ars = Redeem_schemes.objects.create(
                REDEEM              = add ,
                RECORDNO            = recordNo[i] ,
                EXTUNIQUEREFID      = extUniqueRefId[i] ,
                FOLIOACCNO          = folioAccNo[i] ,
                FOLIOCHECKDIGIT     = folioCheckDigit[i] ,
                RTAAMCCODE          = rtaAmcCode[i] ,
                RTASCHEMECODE       = rtaSchemeCode[i] ,
                # DIVIDENDOPTION      = dividendOption ,
                TXNVOLUMETYPE       = txnVolumeType[i] ,
                TXNVOLUME           = txnVolume[i] ,
                PAYOUTFLAG          = payoutFlag[i] ,
                INVACCNO            = invAccNo[i] ,
                MICRNO              = micrNo[i] ,
                IFSCCODE            = ifscCode[i] ,
            )
            if txntype == "J":
                # frequency[i]
                ars.FREQUENCY       = frequency[i]
                ars.DAY             = day[i]
                ars.START_MONTH     = start_Month[i]
                ars.START_YEAR      = start_Year[i]
                ars.END_MONTH       = end_Month[i]
                ars.END_YEAR        = end_Year[i]
            ars.save()
        return JsonResponse("Redeem Add Sucess",safe=False,status=200)
    except Exception as e:
        logger.exception(e)
        return JsonResponse("Something went wrong",safe=False,status=500)
    
    





