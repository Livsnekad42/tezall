POST http://app.tezlombard.kz/auth/loginApi/

    <- {
        password: "..",
        phone: "..",
        app_name: "aqsha"
    }
    
    -> {
        response: true,
        tokenApp: ""
    }
    
    Чтобы войти в личный кабинет делаем GET запрос с tokenApp
        http://app.tezlombard.kz?tokenApp=...

POST http://app.tezlombard.kz/auth/sendSmsApi/
    <- {
        phone: "..",
    }
    
    Будет выслано СМС с кодом
    
    
POST http://app.tezlombard.kz/auth/confirmApi/
    
    <- {
        phone: "..",
        confirmCode: "",
        app_name: "aqsha",
    }
    
    -> {
        response: true,
        tokenApp: ""
    }
    

POST http://app.tezlombard.kz/auth/recovery/
    <- {
        birthDate: "",
        phone: ".."
    }
    
    -> SMS с новым паролем
