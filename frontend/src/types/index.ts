export interface Vehicle {
  modelName: string; 
  year: number;     
  plateNumber: string; 
  kilometers: number; 
  image: string;      
  nextServiceDate: string; 
}

export interface User {
  fullName: string;
  isPremium: boolean;
  phone: string;
  insuranceCompany: string;
  policyNumber: string;
}