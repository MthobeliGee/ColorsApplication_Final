const provinces =  [
    {
      ProvinceName:"KwaZulu-Natal",
      cities:  [
        "Durban",
        "Pietermaritzburg",
        "Newcastle",
        "Richards Bay",
        "Ladysmith",
        "Margate",
        "Port Shepstone",
        "Vryheid",
        "Estcourt",
        "Other"
  
      ]
  
      
    },
    {
      ProvinceName:"Eastern Cape",
      cities:  [
        "Port Elizabeth",
        "East London",
        "Grahamstown",
        "Mthatha",
        "Port Alfred",
        "Queenstown",
        "Uitenhage",
        "Graaff-Reinet",
        "Aliwal North",
        "Bhisho",
        "Other"
  
      ],
    },
    
    { 
      ProvinceName:"Free State",
      cities:[
      "Bloemfontein",
      "Welkom",
      "Bethlehem",
      "Sasolburg",
      "Virginia",
      "Parys",
      "Kroonstad",
      "Phuthaditjhaba",
      "Harrismith",
      "Mangaung",
      "Other"
  
    ]},
    {
    ProvinceName:"Gauteng",
    cities:[
      "Johannesburg",
      "Pretoria",
      "Soweto",
      "Benoni",
      "Vereeniging",
      "Centurion",
      "Tembisa",
      "Krugersdorp",
      "Randburg",
      "Boksburg",
      "Other"
  
    ]},
  
    {
      ProvinceName:"Limpopo",
      cities:[
        "Polokwane",
        "Mokopane",
        "Thohoyandou",
        "Phalaborwa",
        "Tzaneen",
        "Musina",
        "Louis Trichardt",
        "Lebowakgomo",
        "Modimolle",
        "Thabazimbi",
        "Other"
        
      ]
    },
    {
      ProvinceName:"Mpumalanga",
      cities: [
        "Nelspruit",
        "Mbombela",
        "Witbank",
        "Middelburg",
        "Secunda",
        "Ermelo",
        "Standerton",
        "Lydenburg",
        "Barberton",
        "White River",
        "Other"
  
      ]
    },
    {
      
      ProvinceName:"Northern Cape",
      cities:[
        "Kimberley",
        "Upington",
        "Kathu",
        "De Aar",
        "Springbok",
        "Kuruman",
        "Hartswater",
        "Prieska",
        "Colesberg",
        "Postmasburg",
        "Other"
  
      ]
    },
  {
    ProvinceName:"North West",
    cities: [
      "Rustenburg",
      "Mahikeng",
      "Potchefstroom",
      "Klerksdorp",
      "Brits",
      "Orkney",
      "Mmabatho",
      "Lichtenburg",
      "Vryburg",
      "Wolmaransstad",
      "Other"
  
    ]
  },
  
  {
    ProvinceName: "Western Cape",
    cities: [
      "Cape Town",
      "Stellenbosch",
      "George",
      "Paarl",
      "Worcester",
      "Mossel Bay",
      "Oudtshoorn",
      "Knysna",
      "Hermanus",
      "Beaufort West",
      "Other"
  
    ]
  }
  ]
  const keys = Object.keys(provinces);
  
  const drpListProvince = document.getElementById('drpListProvince')
  
  provinces.forEach(function(Province) {
    drpListProvince.innerHTML += '<option value="'+Province.ProvinceName+'">'+Province.ProvinceName+'</option>';
  });
  setCities(drpListProvince.value)
  
  function getCities(provinceName){
    var province1 = provinces.find(function(province) {
      return province.ProvinceName === provinceName;
    });
  
   
    setCities(province1.cities)
  }
  
  
  
  
  
  function setCities(provinceName){
  
  
    const provinceOBJ = provinces.find(province => province.ProvinceName === provinceName/*provinceName"Eastern Cape*/);
  
    const cities = provinceOBJ.cities
  
    const drpCities = document.getElementById("drpCities")
    drpCities.innerHTML =null
    cities.forEach(function(city){
      drpCities.innerHTML +=`<option value="${city}">${city}</option>`
    });
  }
  function whenCitChange(city){
    isOther(city)
  }
  function isOther(city){
    let txt_HostCity_holder = document.getElementById("txt_HostCity_holder")
    let txt_HostCity =  document.getElementById("txt_HostCity")
    let drpCities = document.getElementById("drpCities")
  
  
    if(city === 'Other'){
      txt_HostCity_holder.hidden = false
      txt_HostCity.required = true
      drpCities.required = false
      txt_HostCity.name = 'City'
      drpCities.name =''
    }
    else{
      txt_HostCity_holder.hidden = true
      txt_HostCity.required = false
      drpCities.required = true
      txt_HostCity.name = '';
      drpCities.name='City'
  
    }
  }
  
  function showSnackbar(messagePropertiesObject) {
    var snackbar = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    snackbar.className = "show";
  
    snackbar.className += " "+messagePropertiesObject.type;
    snackbar.innerHTML = messagePropertiesObject.message
    
    // After 3 seconds, remove the "show" class from DIV
    setTimeout(function() {
      snackbar.className = snackbar.className.replace("show", "");
    }, 5000);
  }
  
  
  function validateDate(date, type){
  
    const StartDate = document.getElementById("StartDate")
    //let isFutureDate = i
    if(isFutureDate(date)){
      if(type =='start'){
        document.getElementById("datemsg").hidden = true
  
      }
      else  if(type =='end'){
        document.getElementById("datemsgend").hidden = true
  
      }
    }
    else{
      if(type ==='start'){
        StartDate.value = null
        const datemsg = document.getElementById("datemsg")
        datemsg.innerHTML =`'${date}' is in not valid, dates must be in the future.`
      }
      if(type ==='end'){
        document.getElementById("endDate").value = null;
        const datemsg = document.getElementById("datemsgend")
        datemsg.innerHTML =`'${date}' is in not valid, dates must be in the future.`
      }
    }
    
  
  }
  
  function isFutureDate(dateString) {
    // Convert input string to Date object
    var inputDate = new Date(dateString);
    
    // Get current date
    var currentDate = new Date();
  
    // Compare the input date with the current date
    if (inputDate > currentDate) {
        return true; // Input date is in the future
    } else {
        return false; // Input date is in the past or it's the current date
    }
  }
  
  // Example usage:
  var dateValue = "2024-05-03"; // Your date value
 // Output: false (assuming today is 2024-05-03)
  
  
  
  
  