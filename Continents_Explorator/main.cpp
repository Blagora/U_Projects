#include <iostream>  
#include <string>  
#include <vector>
#include <algorithm>
#include <fstream>

using namespace std;  
struct paises{
        string continente;
        string nombre;
        string capital;
        string presidente;
        int poblacion;
        double superficie;
        string idiomaOficial;
        double densidad;
};
struct continentes{
        string nombrec;
        vector<paises> Pais;
     
        void agregarPais(const paises& regPais){
            Pais.push_back(regPais);
        }
        int verPoblacion(){
            int poblacionT=0;
            for(const auto& paises : Pais){
                poblacionT+=paises.poblacion;
            }
            return poblacionT;
         }
     
         double verSuperficie(){
            double superficieT=0;
            for(const auto& paises : Pais){
                superficieT+=paises.superficie;
            }
            return superficieT;
         }
     
         double verDensidad(){
             double densidadT; 
             densidadT=verPoblacion()/verSuperficie();
             return densidadT;
         }
     
};
void Registrar_continente(vector<continentes> &Rcontinente);
void Registrar_pais(vector<continentes> &Rcontinente);
void Ver_continente(vector<continentes> &Rcontinente);
void Ver_pais(vector<continentes> &Rcontinente);
void Eliminar_continente (vector<continentes> &Rcontinente);
void Eliminar_pais(vector<continentes> &Rcontinente);
void Modificar_continente(vector<continentes> &Rcontinente);
void Modificar_pais(vector<continentes> &Rcontinente);
void Top_población(vector<continentes> &Rcontinente);
void Leer_informacion(vector<continentes> &Rcontinente);
void Actualizar_informacion(vector<continentes> &Rcontinente);

int main() {  
    
    setlocale(LC_ALL,"spanish");
    vector<continentes> Continentes;
    int opcion;
    Leer_informacion(Continentes);
    while (opcion!=10) {  
        
        cout << "Seleccione una opción:" << endl; 
        cout << "1. Registrar un continente" << endl;  
        cout << "2. Registrar un pais" << endl; 
        cout << "3. Ver información de continente" << endl; 
        cout << "4. Ver información de pais" << endl; 
        cout << "5. Eliminar un continente" << endl;  
        cout << "6. Eliminar un pais" << endl; 
        cout << "7. Modificar un continente" << endl; 
        cout << "8. Modificar un pais" << endl; 
        cout << "9. Top 5 paises mas poblados" << endl; 
        cout << "10. Salir" << endl;  
        cout << "Opción: ";  
        cin >> opcion;
        switch (opcion) {  
            case 1: 
                Registrar_continente(Continentes);
                break; 
            case 2:
                Registrar_pais(Continentes);
                break;
            case 3:
                Ver_continente(Continentes);
                break;
            case 4:
                Ver_pais(Continentes);
                break;
            case 5:
                Eliminar_continente(Continentes);
                break;
            case 6:
                Eliminar_pais(Continentes);
                break;
            case 7:
                Modificar_continente(Continentes);
                break;
            case 8:
                Modificar_pais(Continentes);
                break;
            case 9:
                Top_población(Continentes);
                break;
            case 10:
                Actualizar_informacion(Continentes);
                cout << "Saliendo del programa" << endl;
                cout << "       Gracias       " << endl;
                break;
            default: 
                cout << "Opción invalida" << endl;
            }
    }
    return 0;  
} 
// Función para registrar un continente
void Registrar_continente(vector<continentes> &Rcontinente){
    bool continenteExistente=false;
    cin.ignore();
    string nombre;
    cout<<"Digite el nombre del continente: ";
    getline(cin, nombre);
    for(auto& continentes : Rcontinente){
        if(continentes.nombrec==nombre){
            continenteExistente=true;
        }   
    }
    if(nombre.empty()){
        cout<<"Nombre u opción inválida."<<endl;
    }
    else if(continenteExistente){
        cout<<"El Continente ya existe."<<endl;
    }
    else{
        Rcontinente.push_back({nombre,{}});
        cout << "Continente registrado correctamente." << endl;
    }
}
// Función para registrar un país
void Registrar_pais(vector<continentes> &Rcontinente){
    bool paisExistente=false;
    string nombrec;
    double densidad;
    bool found=false;
    cout<<"Digite el nombre del continente a donde guardar el pais: ";
    cin.ignore();
    getline(cin, nombrec);
    for(auto& continentes : Rcontinente){
        if(nombrec==continentes.nombrec){
            string nombre, capital, presidente, idiomaOficial;
            int poblacion;
            double superficie;
            cout << "Ingrese el nombre del país: ";
            getline(cin, nombre);
            for(auto& pais : continentes.Pais){
                if(pais.nombre==nombre){
                    paisExistente=true;
                }
            }
            if(paisExistente==true){
                cout << "El pais ya existe. "<<endl;
            }
            else{
                cout << "Ingrese la capital del país: ";
                getline(cin, capital);
                cout << "Ingrese el nombre del presidente del país: ";
                getline(cin, presidente);
                cout << "Ingrese la población del país: ";
                cin >> poblacion;
                cout << "Ingrese la superficie del país (en Km^2): ";
                cin >> superficie;
                cin.ignore();
                cout << "Ingrese el idioma oficial del país: ";
                getline(cin, idiomaOficial);
                densidad=poblacion/superficie;
                continentes.agregarPais({nombrec,nombre, capital, presidente, poblacion, superficie, idiomaOficial, densidad});
            }
            found=true;
        }
    }
    if(!found){
        cout << "Continente no encontrado." << endl;
    }
}
// Función para visualizar información de un continente
void Ver_continente(vector<continentes> &Rcontinente){
    string nombrec;
    bool found=false;
    cout<<"Digite el nombre del continente a visualizar: ";
    cin.ignore();
    getline(cin, nombrec);
    for(auto& continentes : Rcontinente){
        if(nombrec==continentes.nombrec){
            cout<<"Nombre: "<<continentes.nombrec<<endl;
            cout<<"Paises: ";
            for(const auto& continentes : continentes.Pais){
                cout<<continentes.nombre<<" ";
            }
            cout<<endl;
            cout<<"Poblacion: "<<continentes.verPoblacion()<<endl;
            cout<<"Superficie: "<<continentes.verSuperficie()<<endl;
            cout<<"Densidad: "<<continentes.verDensidad()<<" habitantes por Km^2"<<endl;
            cout<<"Idioma oficial: ";
            for(const auto& continentes : continentes.Pais){
                cout<<continentes.idiomaOficial<<" ";
            }
            cout<<endl;
            found=true;
        }
    }
    if(!found){
        cout << "Continente no encontrado." << endl;
    }
}
void Ver_pais(vector<continentes> &Rcontinente){
    string nombrec, nombrep;
    bool found=false, found2=false;
    cout<<"Digite el nombre del continente al que pertenece el pais: ";
    cin.ignore();
    getline(cin, nombrec);
    for(auto& continentes : Rcontinente){
        if(nombrec==continentes.nombrec){
            cout<<"Digite el nombre del pais: ";
            getline(cin, nombrep);
            for(auto& pais : continentes.Pais){
                if(nombrep==pais.nombre){
                    cout<<"Nombre: "<<pais.nombre<<endl;
                    cout<<"Capital: "<<pais.capital<<endl;
                    cout<<"Presidente: "<<pais.presidente<<endl;
                    cout<<"Poblacion: "<<pais.poblacion<<endl;
                    cout<<"Superficie: "<<pais.superficie<<endl;
                    cout<<"Densidad: "<<pais.densidad<<" habitantes por Km^2"<<endl;
                    cout<<"Idioma oficial: "<<pais.idiomaOficial<<endl;
                   found2=true; 
                }
            }
            found=true;
        }
    }
    if(!found){
        cout << "Continente no encontrado." << endl;
    }
    if(!found2){
        cout << "Pais no encontrado." << endl;
    }
    
}

void Eliminar_continente(vector<continentes> &Rcontinente){
    string nombre_continente;
    cout << "Ingrese el nombre del continente a eliminar: ";
    cin.ignore();
    getline(cin, nombre_continente);

    bool encontrado = false;
    for (auto it = Rcontinente.begin(); it != Rcontinente.end();) {
        if (it->nombrec == nombre_continente) {
            
            it = Rcontinente.erase(it);
            encontrado = true;
        } else {
            ++it;
        }
    }
    if(encontrado)
    {
        cout << "Continente eliminado exitosamente." << endl;
    }
    else{
        cout << "Continente no encontrado." << endl;
    }
}

void Eliminar_pais(vector<continentes> &Rcontinente){
    string nombre_continente;
    string nombre_pais;
    cout << "Ingrese el nombre del continente al que pertenece el país: ";
    cin.ignore();
    getline(cin, nombre_continente);
    cout << "Ingrese el nombre del país a eliminar: ";
    getline(cin, nombre_pais);
    bool encontrado_continente = false;
    for (auto& continente : Rcontinente) {
        if (continente.nombrec == nombre_continente) {
            encontrado_continente = true;
            bool encontrado_pais = false;
            for (auto it = continente.Pais.begin(); it != continente.Pais.end();) {
                if (it->nombre == nombre_pais) {
                    it = continente.Pais.erase(it);
                    encontrado_pais = true;
                    cout << "País eliminado exitosamente." << endl;
                } else {
                    ++it;
                }
            }
            if (!encontrado_pais) {
                cout << "El país especificado no fue encontrado en este continente." << endl;
            }
            break; 
        }
    }

    if (!encontrado_continente) {
        cout << "El continente especificado no fue encontrado." << endl;
    }
}

void Modificar_continente(vector<continentes> &Rcontinente){
    string nombre_continente_viejo;
    string nombre_continente_nuevo;
    cout << "Ingrese el nombre del continente que desea modificar: ";
    cin.ignore();
    getline(cin, nombre_continente_viejo);
    cout << "Ingrese el nuevo nombre para el continente: ";
    getline(cin, nombre_continente_nuevo);

    bool encontrado = false;
    for(auto& continente : Rcontinente){
        if (continente.nombrec == nombre_continente_viejo) {
            continente.nombrec = nombre_continente_nuevo;
            encontrado = true;
            cout << "Nombre del continente modificado exitosamente." << endl;
            break;
        }
    }
    if(!encontrado){
        cout << "El continente especificado no fue encontrado." << endl;
    }
}

void Modificar_pais(vector<continentes> &Rcontinente){
    string nombre_continente;
    string nombre_pais;
    cout << "Ingrese el nombre del continente al que pertenece el país que desea modificar: ";
    cin.ignore();
    getline(cin, nombre_continente);
    cout << "Ingrese el nombre del país que desea modificar: ";
    getline(cin, nombre_pais);
    bool encontrado_continente = false;
    for (auto& continente : Rcontinente) {
        if (continente.nombrec == nombre_continente) {
            encontrado_continente = true;
            bool encontrado_pais = false;
            for (auto& pais : continente.Pais) {
                if (pais.nombre == nombre_pais) {
                    encontrado_pais = true;
                    cout << "Ingrese el nuevo nombre del país: ";
                    getline(cin, pais.nombre);
                    cout << "Ingrese la nueva capital del país: ";
                    getline(cin, pais.capital);
                    cout << "Ingrese el nuevo presidente del país: ";
                    getline(cin, pais.presidente);
                    cout << "Ingrese la nueva población del país: ";
                    cin >> pais.poblacion;
                    cout << "Ingrese la nueva superficie del país (en Km^2): ";
                    cin >> pais.superficie;
                    cin.ignore();
                    cout << "Ingrese el nuevo idioma oficial del país: ";
                    getline(cin, pais.idiomaOficial);
                    pais.densidad = pais.poblacion / pais.superficie;
                    cout << "Datos del país modificados exitosamente." << endl;
                    break;
                }
            }
            if (!encontrado_pais) {
                cout << "El país especificado no fue encontrado en este continente." << endl;
            }
            break;
        }
    }
    if (!encontrado_continente) {
        cout << "El continente especificado no fue encontrado." << endl;
    }
}
void Top_población(vector<continentes> &Rcontinente){
    vector<int> poblaciones;
    int topIndice[5];
    string topNombre[5];
    int posicion, posicionDef;
    for(auto continentes : Rcontinente){
        for(auto paises : continentes.Pais){
            poblaciones.push_back(paises.poblacion);
        }
    }
    sort(poblaciones.rbegin(), poblaciones.rend());
    for(int i=0;i<5;i++){
        topIndice[i]=poblaciones[i];
    }
    cout<<"Los paises mas poblados son: ";
    for(int i=0;i<5;i++){
        for(auto continentes : Rcontinente){
            for(auto paises : continentes.Pais){
                if(topIndice[i]==paises.poblacion){
                    topNombre[i]=paises.nombre;
                    cout<<topNombre[i]<<" ";
                }
            }
        }
    }
    cout<<endl;
    
}
void Leer_informacion(vector<continentes> &Rcontinente){
    ifstream archivoConCSV, archivoPaisCSV;
    int i=0;
    string contenedorContinentes, contenedorPaises, continente;
    archivoConCSV.open("Continentes.txt", ios::in);
    if(archivoConCSV.is_open()){
        getline(archivoConCSV, contenedorContinentes);
        while(i<=contenedorContinentes.length()){
            if(contenedorContinentes[i]==','||i==contenedorContinentes.size()){
                Rcontinente.push_back({continente,{}});
                continente="";
            }
            else{
                continente+=contenedorContinentes[i];
            }
            i++;
        }
        archivoConCSV.close();
    }
    else{
        cout<<"El archivo contientes no pudo abrirse. ";
    }
    archivoPaisCSV.open("Paises.txt", ios::in);
    if(archivoPaisCSV.is_open()){
        while(getline(archivoPaisCSV, contenedorPaises)){
            i=0;
            string nombrec, nombre, capital, presidente, idiomaOficial, texto;
            int poblacion, contador=0;
            double superficie, densidad;
            while(i<=contenedorPaises.length()){
                if(contenedorPaises[i]==',' && contador==0){
                    nombrec=texto;
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]==',' && contador==1){
                    nombre=texto;
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]==',' && contador==2){
                    capital=texto;
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]==',' && contador==3){
                    presidente=texto;
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]==',' && contador==4){
                    poblacion=stoi(texto);
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]==',' && contador==5){
                    superficie=stod(texto);
                    texto="";
                    contador++;
                }
                else if(contenedorPaises[i]<=contenedorPaises.length() && contador==7){
                    idiomaOficial=texto;
                    texto="";
                    contador++;
                }
                else{
                    texto+=contenedorPaises[i];
                }
                i++;
            }
            densidad=poblacion/superficie;
            for(auto& pais : Rcontinente){
                if(pais.nombrec==nombrec){
                    pais.agregarPais({nombrec,nombre,capital,presidente,poblacion,superficie,idiomaOficial,densidad});
                    break;
                }
            }
        }
        archivoPaisCSV.close();
    }
    else{
        cout<<"El archivo paises no pudo abrirse. ";
    }
}
void Actualizar_informacion(vector<continentes> &Rcontinente){
    ofstream archivoConCSV;
    int contador, ultimoValor;
    archivoConCSV.open("Continentes.txt", ios::out);
    if(archivoConCSV.is_open()){
        for(auto Continentes : Rcontinente){
            contador++;
        }
        for(auto Continentes : Rcontinente){
            if(contador-1==ultimoValor){
                archivoConCSV<<Continentes.nombrec;
            }
            else{
                archivoConCSV<<Continentes.nombrec<<",";
            }
            ultimoValor++;
        }
        archivoConCSV.close();
    }
    else{
        cout<<"El archivo contientes no pudo abrirse. ";
    }
    ofstream archivoPaisCSV;
    archivoPaisCSV.open("Paises.txt", ios::out);
    if(archivoPaisCSV.is_open()){
        for(auto continentes : Rcontinente){
           for(auto paises : continentes.Pais){
                archivoPaisCSV<<paises.continente<<","<<
                paises.nombre<<","<<
                paises.capital<<","<<
                paises.presidente<<","<<
                paises.poblacion<<","<<
                paises.superficie<<","<<
                paises.densidad<<","<<
                paises.idiomaOficial<<endl;
            }
        }
        archivoPaisCSV.close();
    }
    else{
        cout<<"El archivo paises no pudo abrirse. ";
    }
    
}







