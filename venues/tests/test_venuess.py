from django.contrib.gis.geos.point import Point
from django.core.urlresolvers import reverse
from restaurant.utils import TestCaseEx
from venues.models.cuisine import Cuisine
from venues.models.restaurant import Restaurant
from venues.tests import TestCaseVenue

__author__ = 'm'


class TestVenuess(TestCaseVenue):
    def setUp(self):
        super(TestVenuess, self).setUp()

        self.cuisine = Cuisine.objects.create(name="cuisine")

        self.approvedRestaurant = Restaurant(name="Approved",
                                             approved=True, location=Point(0, 0))
        self.approvedRestaurant.save()
        self.approvedRestaurant.cuisines.add(self.cuisine)
        self.approvedRestaurant.save()

        self.approvedFarAwayRestaurant = Restaurant(name="approvedFarAwayRestaurant",
                                                    approved=True, location=Point(45, 45))
        self.approvedFarAwayRestaurant.save()
        self.approvedFarAwayRestaurant.cuisines.add(self.cuisine)
        self.approvedFarAwayRestaurant.save()

        self.approvedRestaurantWithoutCategory = Restaurant(name="WithoutCategory",
                                                            approved=True, location=Point(0, 0))
        self.approvedRestaurantWithoutCategory.save()

        self.restaurant = Restaurant(name="UnApproved",
                                     approved=False, location=Point(0, 0))
        self.restaurant.save()
        self.restaurant.cuisines.add(self.cuisine)
        self.restaurant.save()


    def test_anyone_can_access_index_page(self):
        self.can_get("venues.views.venuess.index")

    def test_guest_can_see_only_approved_restaurants(self):
        response = self.can_get("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)

        response = self.can_post("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)

    @TestCaseEx.login
    def test_simple_user_can_see_only_approved_restaurants(self):
        response = self.can_get("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)

        response = self.can_post("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)

    @TestCaseVenue.moderator
    def test_moderator_can_see_all_restaurants(self):
        response = self.can_get("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertContains(response, self.restaurant.name)

        response = self.can_post("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertContains(response, self.restaurant.name)

    @TestCaseEx.superuser
    def test_superuser_can_see_all_restaurants(self):
        response = self.can_get("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertContains(response, self.restaurant.name)

        response = self.can_post("venues.views.venuess.index")
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertContains(response, self.restaurant.name)

    # def test_closets_should_respond(self):
    #     self.can_get("venues.views.venuess.closest")

    def test_closest_should_respond_with_lat_and_lng_parameters(self):
        response = self.can_get("venues.views.venuess.index", params={
            'lat': 0,
            'lon': 0
        })
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertContains(response, self.approvedRestaurantWithoutCategory.name)
        self.assertNotContains(response, self.approvedFarAwayRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)


    def test_closest_should_respond_with_lat_and_lng_and_categories_parameters(self):
        response = self.can_get("venues.views.venuess.index", params={
            'lat': 0,
            'lon': 0,
            'category': self.cuisine.name
        })
        self.assertContains(response, self.approvedRestaurant.name)
        self.assertNotContains(response, self.approvedRestaurantWithoutCategory.name)
        self.assertNotContains(response, self.approvedFarAwayRestaurant.name)
        self.assertNotContains(response, self.restaurant.name)

    def test_anyone_can_see_approved_restaurant(self):
        self.can_get("venues.views.venuess.restaurant", pargs=[self.approvedRestaurant.pk])

    def test_guest_cant_see_unapproved_restaurant(self):
        response = self.get("venues.views.venuess.restaurant", pargs=[self.restaurant.pk])
        self.assertEqual(response.status_code, 404)

    @TestCaseVenue.login
    def test_simple_user_CANT_see_unapproved_NOT_his_restaurant(self):
        response = self.get("venues.views.venuess.restaurant", pargs=[self.restaurant.pk])
        self.assertEqual(response.status_code, 404)

    @TestCaseVenue.login
    def test_simple_user_CAN_see_unapproved_his_restaurant(self):
        r = Restaurant(approved=True, created_by=self.user)
        r.save()
        self.can_get("venues.views.venuess.restaurant", pargs=[r.pk])

    @TestCaseVenue.moderator
    def test_moderator_CAN_see_any_restaurant(self):
        r = Restaurant(approved=True, created_by=self.user)
        r.save()
        self.can_get("venues.views.venuess.restaurant", pargs=[r.pk])
        self.can_get("venues.views.venuess.restaurant", pargs=[self.approvedRestaurant.pk])
        self.can_get("venues.views.venuess.restaurant", pargs=[self.restaurant.pk])

    @TestCaseVenue.superuser
    def test_superuser_CAN_see_any_restaurant(self):
        r = Restaurant(approved=True, created_by=self.user)
        r.save()
        self.can_get("venues.views.venuess.restaurant", pargs=[r.pk])
        self.can_get("venues.views.venuess.restaurant", pargs=[self.approvedRestaurant.pk])
        self.can_get("venues.views.venuess.restaurant", pargs=[self.restaurant.pk])

    def test_guest_CANT_remove_restaurant(self):
        r = Restaurant(created_by=self.user, name='alskdlasdllasjdlk')
        r.save()
        self.redirect_to_login_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

    @TestCaseVenue.login
    def test_simple_user_CANT_remove_not_his_restaurant(self):
        r = Restaurant(name='alskdlasdllzxcaasjdlk')
        r.save()
        self.redirect_to_login_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

    @TestCaseVenue.login
    def test_simple_user_CANT_remove_his_approved_restaurant(self):
        r = Restaurant(created_by=self.user, approved=True, name='alskdasdzxlasdllasjdlk')
        r.save()
        self.redirect_to_login_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

    @TestCaseVenue.login
    def test_simple_user_CAN_remove_his_not_approved_restaurant(self):
        r = Restaurant(created_by=self.user, approved=False, name='alsasdkdlasdllasjdlk')
        r.save()
        self.redirect_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

        self.assertEqual(Restaurant.objects.filter(pk=r.pk).count(), 0)

    @TestCaseVenue.moderator
    def test_moderator_CAN_remove_any_restaurant(self):
        r = Restaurant(created_by=self.user, approved=True, name='alskdlasdllasjdlk')
        r.save()
        self.redirect_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

        self.assertEqual(Restaurant.objects.filter(pk=r.pk).count(), 0)

    @TestCaseVenue.superuser
    def test_superuser_CAN_remove_any_restaurant(self):
        r = Restaurant(created_by=self.user, approved=True, name='alskdlasdllasjdlk')
        r.save()
        self.redirect_on_get("venues.views.venuess.suspend_restaurant", pargs=[r.pk])

        self.assertEqual(Restaurant.objects.filter(pk=r.pk).count(), 0)

    def test_guest_cant_add_restaurant(self):
        self.redirect_to_login_on_get("venues.views.venuess.add_restaurant")

    @TestCaseVenue.login
    def test_user_can_add_restaurant(self):
        self.can_get("venues.views.venuess.add_restaurant")

        params = {
            'name': 'alksjdlas',
            'address': 'laksdlkasd',
            'cuisines': self.cuisine.pk,
            'catering': True,
            'delivery': True,
            'alcoholFree': True,
            'porkFree': True,
            'muslimOwner': True,
            'location': str(Point(0,0)),
            'menu': 1,
            'city': 'kalsjd',
            'country': 'RU',
            'website': 'http://site.ru/',
        }

        count_before = Restaurant.objects.count()

        response = self.redirect_on_post("venues.views.venuess.add_restaurant", params=params)

        self.assertEqual(count_before + 1, Restaurant.objects.count() )
        rest = Restaurant.objects.order_by('-pk').first()

        for key in params.keys():
            if key == 'cuisines':
                self.assertEqual(rest.cuisines.all()[0].pk, self.cuisine.pk)
            else:
                self.assertEqual(getattr(rest, key), params[key])

    def test_guest_cant_update_restaurant(self):
        self.redirect_to_login_on_get("venues.views.venuess.update_restaurant", pargs=[self.approvedRestaurant.pk])

    @TestCaseVenue.login
    def test_user_CANT_update_not_his_restaurant(self):
        r = Restaurant()
        r.save()

        cuisine = Cuisine.objects.create(name="nasjdasdashaksds62a")


        params = {
            'name': 'alksjdlas',
            'address': 'laksdlkasd',
            'cuisines': cuisine.pk,
            'catering': True,
            'delivery': True,
            'alcoholFree': True,
            'porkFree': True,
            'muslimOwner': True,
            'location': str(Point(0,0)),
            'menu': 1,
            'city': 'kalsjd',
            'country': 'RU',
            'website': 'http://site.ru/',
        }

        self.redirect_to_login_on_get("venues.views.venuess.update_restaurant", pargs=[r.pk], params=params)

    @TestCaseVenue.moderator
    def test_moderator_CAN_update_any_restaurant(self):
        r = Restaurant(name="lasjdklasd,.mxz,calsd")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashakssdsa")
        Cuisine.objects.create(name="nasjdasdashaksddsa")
        Cuisine.objects.create(name="nasjdasdashaksdasa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdasa")
        Cuisine.objects.create(name="nasjdasdashaksdsdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashakshgdsa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksdfsa")
        Cuisine.objects.create(name="nasjdasdashaksddsa")
        Cuisine.objects.create(name="nasjdasdashakdssdsa")
        Cuisine.objects.create(name="nasjdasdashaksvdsa")
        Cuisine.objects.create(name="nasjdasdashaks2dsa")
        Cuisine.objects.create(name="nasjdasdashaks3dsa")
        Cuisine.objects.create(name="nasjdasdashaks32dsa")
        Cuisine.objects.create(name="nasjdasdashaksd2sa")
        Cuisine.objects.create(name="nasjdasdashaksd23sa")
        Cuisine.objects.create(name="nasjdasdashaksd2sa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        Cuisine.objects.create(name="nasjdasdashaksd521sa")
        Cuisine.objects.create(name="nasjdasdashaksdsa")
        cuisine = Cuisine.objects.create(name="nasjdhaksdsa")
        r.save()

        params = {
            'name': 'alksjdlas',
            'address': 'laksdlkasd',
            'cuisines': cuisine.pk,
            'catering': True,
            'delivery': True,
            'alcoholFree': True,
            'porkFree': True,
            'muslimOwner': True,
            'location': str(Point(0,0)),
            'menu': 1,
            'city': 'kalsjd',
            'country': 'RU',
            'website': 'http://site.ru/',
        }

        self.can_get("venues.views.venuess.update_restaurant", pargs=[r.pk])
        response = self.redirect_on_post("venues.views.venuess.update_restaurant", pargs=[r.pk], params=params)

        r = Restaurant.objects.get(pk=r.pk)

        for key in params.keys():
            if key == 'cuisines':
                self.assertEqual(r.cuisines.all()[0].pk, cuisine.pk)
            else:
                self.assertEqual(getattr(r, key), params[key])

    def test_anyone_can_get_restaurant_by_slug(self):
        self.can_get("venues.views.venuess.restaurant_by_slug", pargs=[self.approvedRestaurant.slug])

