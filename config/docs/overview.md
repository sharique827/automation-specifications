# ONDC:TRV10 2.0.1 — Overview

## Summary

ONDC:TRV10 enables ride-hailing services to be transacted across the Open Network for Digital Commerce, allowing passengers to discover and book rides from multiple cab operators through a single buyer application. Instead of using isolated platforms like Ola or Uber, passengers can access all registered ride-hailing providers through ONDC, and multiple service providers can offer their rides to the same passenger audience through the network.

## Sector & Purpose

**Sector:** Ride-hailing and on-demand mobility

**Problem solved:** This domain solves the problem of booking rides via the ONDC network. It enables ride-hailing platforms—such as Ola, Uber, and other cab service providers registered on ONDC—to share their ride-hailing services across the network. Rather than each platform maintaining separate user bases and applications, providers can offer their services to buyers through ONDC, and buyers can discover and compare rides from multiple operators without switching applications.

## Real-World Actors

- **Passengers/Riders:** People who want to book a cab for a journey. They use a buyer application connected to ONDC to search, compare, and book rides.
- **Ride-hailing Service Providers:** Platforms like Ola, Uber, and other registered ONDC-enabled cab operators that provide driver and vehicle resources.
- **Drivers:** Individuals who operate the vehicles and execute the ride bookings.
- **ONDC Network:** The infrastructure enabling discovery and transaction between riders and service providers.

## Use Cases

- On-demand ride booking and driver assignment
- Driver assignment at the time of confirmation (on-confirm) or after confirmation (post-confirm)
- Self-pickup ride options
- Female driver selection and assignment
- Ride cancellation by either rider or driver
- Journey progress updates during a trip
- Technical cancellation handling

## Key Concepts

- **Ride-hailing:** The service of booking and paying for a ride on-demand via a digital platform.
- **Taxi/Cab:** The vehicle type being transacted—typically a standardized vehicle for hire.
- **On-demand matching:** Real-time matching of riders with available drivers and vehicles.
- **Multi-provider network:** Multiple competing ride-hailing operators (Ola, Uber, etc.) offering services through a single buyer interface.
- **Driver assignment flow:** The process of assigning an available driver to a confirmed booking.

## Example Scenario

A customer wants to book a cab for a journey. Instead of opening the Ola app, the Uber app, or any other individual ride-hailing platform, they open their ONDC-enabled buyer application. They enter their pickup and drop-off locations. The application searches across all ride-hailing providers connected to ONDC—including Ola, Uber, and other registered operators—and displays available rides with different pricing, vehicle types, and driver options. The customer selects a female driver option from one provider. The ride is confirmed, a driver is assigned from that provider's fleet, and the customer receives live updates as the driver approaches, during the journey, and when the ride completes. Throughout this transaction, the customer never left a single application, and the ride-hailing provider used ONDC to access riders they might not have reached directly.
