package hello;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
public class HelloController {

  @RequestMapping("/hello")
  public String hello() {
    return "Hello world!";
  }
  @RequestMapping("/health")
  public String health() {
    return "Ok";
  }
}
