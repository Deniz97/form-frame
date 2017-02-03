


$scope.LoginContext = {
            KullaniciAdi: localStorage.KullaniciAdi,
            Sifre: localStorage.Sifre,
            BeniHatirla: isUndefined(localStorage.BeniHatirla) ? false : localStorage.BeniHatirla=="true"
        };