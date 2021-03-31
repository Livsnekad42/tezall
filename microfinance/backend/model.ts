export interface PawnTicket {
   id?: number
   issueDate?: Date
   returnDate?: Date
   guaranteeDate?: Date
   creditSum?: number
   lastPaymentDate?: Date
   creditPeriod?: number
   saldoSum?: number
   interestSum?: number
   penaltySum?: number
   totalSum?: number
   totalSumOnReturnDate?: number
   status?: string
}


export interface PawnTicketOperations {
   operDate?: Date
   operType?: string
   operSum?: number
   operPlace?: string
}


export interface PawnProperty {
   propertyId?: number
   positionNumber?: number
   name?: string
}


export interface PawnProperties {
   positionNumber?: number
   name?: string
   description?: string
}


